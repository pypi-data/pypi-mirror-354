import pandas as pd
import numpy as np
from scipy.stats import norm
from datetime import datetime, timedelta
from persiantools.jdatetime import JalaliDate

def option_speculation(
    symbol_underlying: str = "اهرم",  
    long_target: int = None, 
    short_target: int = None,
    status: str = "all",  # می‌تواند یکی از مقادیر "all", "itm", "otm", "deep_itm", "itm", "little_itm", "little_otm", "otm", "deep_otm" باشد
    high_value: bool = False,
    min_days_remaining: int = None,
    max_days_remaining: int = None,
    risk_free_rate: float = 0.2,
    dividend_yield_ratio: float = 0.0,
    volatility_input: float | str = "hv",
    volatility_period_months: int = 12,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    from arb_tehran_finance.tse.tse_report import option_contract, stock_values

    long_positions = None
    short_positions = None

    today_jdate = JalaliDate.today()
    # تبدیل تعداد ماه به روز (تقریبی 30 روز در هر ماه)
    days_for_volatility = volatility_period_months * 30
    start_date = today_jdate - timedelta(days=days_for_volatility)

    df_price = stock_values(
        stock=symbol_underlying,
        start_date=str(start_date),
        end_date=str(today_jdate),
        ignore_date=False,
        adjust_price=True,
        show_weekday=False,
        double_date=False
    )
    df_price = df_price.sort_values('J-Date')
    df_price['daily_return'] = df_price['Adj Close'].pct_change()
    daily_volatility = df_price['daily_return'].std()
    historical_volatility = daily_volatility * np.sqrt(252)

    if isinstance(volatility_input, (int, float)) and volatility_input > 0:
        annual_volatility = volatility_input
    else:
        annual_volatility = historical_volatility


    option_data = option_contract(symbol_underlying=symbol_underlying, option="all")

    option_data['close price (underlying) %'] = ((option_data["close price (underlying)"] - option_data["yesterday price (underlying)"]) / option_data["yesterday price (underlying)"] * 100).round(2)
    option_data["close price (call) %"] = ((option_data["close price (call)"] - option_data["yesterday price (call)"]) / option_data["yesterday price (call)"] * 100).round(2)
    option_data["close price (put) %"] = ((option_data["close price (put)"] - option_data["yesterday price (put)"]) / option_data["yesterday price (put)"] * 100).round(2)

    # محاسبه RoR (underlying) برای موقعیت‌های long و short به صورت جداگانه
    if long_target is not None:
        option_data['RoR (underlying) long'] = ((long_target - option_data["close price (underlying)"]) / option_data["close price (underlying)"] * 100).round(2)
    if short_target is not None:
        option_data['RoR (underlying) short'] = ((short_target - option_data["close price (underlying)"]) / option_data["close price (underlying)"] * 100).round(2)

    # محاسبه نسبت قیمت فعلی به قیمت اعمال برای تعیین وضعیت دقیق‌تر
    option_data['moneyness_ratio'] = (option_data['close price (underlying)'] / option_data['strike price']).round(4)
    
    # تعیین وضعیت دقیق‌تر برای قراردادهای call
    def determine_call_status(moneyness_ratio):
        if moneyness_ratio >= 1.15:  # بیش از 15% بالاتر از قیمت اعمال
            return 'deep_itm'
        elif 1.05 <= moneyness_ratio < 1.15:  # بین 5% تا 15% بالاتر از قیمت اعمال
            return 'itm'
        elif 1.00 <= moneyness_ratio < 1.05:  # تا 5% بالاتر از قیمت اعمال
            return 'little_itm'
        elif 0.95 <= moneyness_ratio < 1.00:  # تا 5% پایین‌تر از قیمت اعمال
            return 'little_otm'
        elif 0.85 <= moneyness_ratio < 0.95:  # بین 5% تا 15% پایین‌تر از قیمت اعمال
            return 'otm'
        else:  # بیش از 15% پایین‌تر از قیمت اعمال
            return 'deep_otm'
    
    # تعیین وضعیت دقیق‌تر برای قراردادهای put
    def determine_put_status(moneyness_ratio):
        if moneyness_ratio <= 0.85:  # بیش از 15% پایین‌تر از قیمت اعمال
            return 'deep_itm'
        elif 0.85 < moneyness_ratio <= 0.95:  # بین 5% تا 15% پایین‌تر از قیمت اعمال
            return 'itm'
        elif 0.95 < moneyness_ratio <= 1.00:  # تا 5% پایین‌تر از قیمت اعمال
            return 'little_itm'
        elif 1.00 < moneyness_ratio <= 1.05:  # تا 5% بالاتر از قیمت اعمال
            return 'little_otm'
        elif 1.05 < moneyness_ratio <= 1.15:  # بین 5% تا 15% بالاتر از قیمت اعمال
            return 'otm'
        else:  # بیش از 15% بالاتر از قیمت اعمال
            return 'deep_otm'
    
    option_data['detailed_status (call)'] = option_data['moneyness_ratio'].apply(determine_call_status)
    option_data['detailed_status (put)'] = option_data['moneyness_ratio'].apply(determine_put_status)
    
    # حفظ ستون‌های قدیمی status برای سازگاری با کدهای قبلی
    option_data['status (call)'] = option_data.apply(lambda row: 'itm' if row['moneyness_ratio'] >= 1.00 else 'otm', axis=1)
    option_data['status (put)'] = option_data.apply(lambda row: 'itm' if row['moneyness_ratio'] <= 1.00 else 'otm', axis=1)

    if high_value:
        avg_value_call = option_data['notional value (call)'].mean(skipna=True)
        avg_value_put = option_data['notional value (put)'].mean(skipna=True)
        option_data = option_data[
            (option_data['notional value (call)'].notna() & (option_data['notional value (call)'] > avg_value_call)) |
            (option_data['notional value (put)'].notna() & (option_data['notional value (put)'] > avg_value_put))
        ]

    if min_days_remaining is not None:
        option_data = option_data[option_data['remained day'] >= min_days_remaining]
    if max_days_remaining is not None:
        option_data = option_data[option_data['remained day'] <= max_days_remaining]

    def black_scholes_value(S, K, T, r, sigma, q, option_type='call'):
        if T <= 0 or S <= 0 or K <= 0 or sigma <= 0:
            return np.nan
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        if option_type == 'call':
            return S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
        elif option_type == 'put':
            return K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
        else:
            return np.nan
    
    # توابع محاسبه پارامترهای یونانی
    def calculate_delta(S, K, T, r, sigma, q, option_type='call'):
        if T <= 0 or S <= 0 or K <= 0 or sigma <= 0:
            return np.nan
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        if option_type == 'call':
            return np.exp(-q * T) * norm.cdf(d1)
        elif option_type == 'put':
            return np.exp(-q * T) * (norm.cdf(d1) - 1)
        else:
            return np.nan
    
    def calculate_gamma(S, K, T, r, sigma, q):
        if T <= 0 or S <= 0 or K <= 0 or sigma <= 0:
            return np.nan
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        return np.exp(-q * T) * norm.pdf(d1) / (S * sigma * np.sqrt(T))
    
    def calculate_theta(S, K, T, r, sigma, q, option_type='call'):
        if T <= 0 or S <= 0 or K <= 0 or sigma <= 0:
            return np.nan
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type == 'call':
            theta = -np.exp(-q * T) * S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm.cdf(d2) + q * S * np.exp(-q * T) * norm.cdf(d1)
        elif option_type == 'put':
            theta = -np.exp(-q * T) * S * norm.pdf(d1) * sigma / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm.cdf(-d2) - q * S * np.exp(-q * T) * norm.cdf(-d1)
        else:
            return np.nan
        
        # تبدیل به مقدار روزانه (تقسیم بر 365)
        return theta / 365
    
    def calculate_vega(S, K, T, r, sigma, q):
        if T <= 0 or S <= 0 or K <= 0 or sigma <= 0:
            return np.nan
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        return S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T) / 100  # تقسیم بر 100 برای تغییر 1% در نوسان‌پذیری
    
    def calculate_rho(S, K, T, r, sigma, q, option_type='call'):
        if T <= 0 or S <= 0 or K <= 0 or sigma <= 0:
            return np.nan
        d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        
        if option_type == 'call':
            return K * T * np.exp(-r * T) * norm.cdf(d2) / 100  # تقسیم بر 100 برای تغییر 1% در نرخ بهره
        elif option_type == 'put':
            return -K * T * np.exp(-r * T) * norm.cdf(-d2) / 100
        else:
            return np.nan

    def implied_volatility(
        market_price, S, K, T, r, q, option_type='call', tol=1e-5, max_iter=100
    ):
        # بررسی اولیه ورودی‌ها
        if any([
            market_price is None or market_price <= 0,
            S is None or S <= 0,
            K is None or K <= 0,
            T is None or T <= 0,
            np.isnan(market_price) or np.isnan(S) or np.isnan(K) or np.isnan(T)
        ]):
            return np.nan

        sigma = 0.3  # حدس اولیه
        for _ in range(max_iter):
            price = black_scholes_value(S, K, T, r, sigma, q, option_type)
            if price is None or np.isnan(price):
                return np.nan

            d1 = (np.log(S / K) + (r - q + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
            vega = S * np.exp(-q * T) * norm.pdf(d1) * np.sqrt(T)

            # محدود کردن sigma در بازه 0.01 تا 3
            sigma = max(0.01, min(sigma, 3.0))

            if vega == 0:
                return np.nan

            # به‌روزرسانی sigma با روش نیوتن-رافسون
            sigma_new = sigma - (price - market_price) / vega

            # اگر تغییر خیلی کم بود، خروج
            if abs(sigma_new - sigma) < tol:
                return sigma_new

            sigma = sigma_new

        # اگر همگرا نشد، NaN برگردان
        return np.nan


    option_data['T'] = option_data['remained day'] / 252
    option_data['implied volatility (call)'] = option_data.apply(
        lambda row: implied_volatility(row['close price (call)'], row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, dividend_yield_ratio, 'call'), axis=1)
    option_data['Black-Scholes value (call)'] = option_data.apply(
        lambda row: black_scholes_value(row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, annual_volatility, dividend_yield_ratio, 'call'), axis=1)
    option_data['valuation status (call)'] = option_data.apply(
        lambda row: 'undervalued' if row['Black-Scholes value (call)'] > row['close price (call)'] else 'overvalued', axis=1)
    
    # محاسبه پارامترهای یونانی برای قراردادهای call
    option_data['delta (call)'] = option_data.apply(
        lambda row: calculate_delta(row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, annual_volatility, dividend_yield_ratio, 'call'), axis=1).round(4)
    option_data['gamma (call)'] = option_data.apply(
        lambda row: calculate_gamma(row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, annual_volatility, dividend_yield_ratio), axis=1).round(6)
    option_data['theta (call)'] = option_data.apply(
        lambda row: calculate_theta(row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, annual_volatility, dividend_yield_ratio, 'call'), axis=1).round(2)
    option_data['vega (call)'] = option_data.apply(
        lambda row: calculate_vega(row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, annual_volatility, dividend_yield_ratio), axis=1).round(2)
    option_data['rho (call)'] = option_data.apply(
        lambda row: calculate_rho(row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, annual_volatility, dividend_yield_ratio, 'call'), axis=1).round(2)

    option_data['implied volatility (put)'] = option_data.apply(
        lambda row: implied_volatility(row['close price (put)'], row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, dividend_yield_ratio, 'put'), axis=1)
    option_data['Black-Scholes value (put)'] = option_data.apply(
        lambda row: black_scholes_value(row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, annual_volatility, dividend_yield_ratio, 'put'), axis=1)
    option_data['valuation status (put)'] = option_data.apply(
        lambda row: 'undervalued' if row['Black-Scholes value (put)'] > row['close price (put)'] else 'overvalued', axis=1)
    
    # محاسبه پارامترهای یونانی برای قراردادهای put
    option_data['delta (put)'] = option_data.apply(
        lambda row: calculate_delta(row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, annual_volatility, dividend_yield_ratio, 'put'), axis=1).round(4)
    option_data['gamma (put)'] = option_data.apply(
        lambda row: calculate_gamma(row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, annual_volatility, dividend_yield_ratio), axis=1).round(6)
    option_data['theta (put)'] = option_data.apply(
        lambda row: calculate_theta(row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, annual_volatility, dividend_yield_ratio, 'put'), axis=1).round(2)
    option_data['vega (put)'] = option_data.apply(
        lambda row: calculate_vega(row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, annual_volatility, dividend_yield_ratio), axis=1).round(2)
    option_data['rho (put)'] = option_data.apply(
        lambda row: calculate_rho(row['close price (underlying)'], row['strike price'], row['T'], risk_free_rate, annual_volatility, dividend_yield_ratio, 'put'), axis=1).round(2)

    # فیلتر کردن بر اساس پارامتر status
    if status != "all":
        # برای قراردادهای call
        if status in ["itm", "otm"]:  # حالت‌های قدیمی برای سازگاری با کدهای قبلی
            call_filter = option_data['status (call)'] == status
            put_filter = option_data['status (put)'] == status
        else:  # حالت‌های جدید و دقیق‌تر
            call_filter = option_data['detailed_status (call)'] == status
            put_filter = option_data['detailed_status (put)'] == status
        
        # اعمال فیلتر مناسب بر اساس نوع قرارداد
        option_data_call_filtered = option_data[call_filter]
        option_data_put_filtered = option_data[put_filter]
        
        # ترکیب نتایج برای حفظ ساختار اصلی دیتافریم
        option_data = pd.concat([option_data_call_filtered, option_data_put_filtered]).drop_duplicates()

    if long_target is not None:
        long_data = option_data.copy()
        
        long_data = long_data[[ 
            'symbol underlying', 'remained day', 'strike price', 'close price (underlying)', 'close price (underlying) %', 'RoR (underlying) long', 
            'contract symbol (call)', 'contract name (call)', 'value (call)', 'notional value (call)', 'open interest (call)', 
            'close price (call)', 'close price (call) %', 'status (call)', 'detailed_status (call)',
            'implied volatility (call)', 'Black-Scholes value (call)', 'valuation status (call)',
            'delta (call)', 'gamma (call)', 'theta (call)', 'vega (call)', 'rho (call)'
        ]].copy()

        long_data['breakeven price (call)'] = long_data['strike price'] + long_data['close price (call)']
        long_data['RoR (call)'] = (((long_target - long_data['breakeven price (call)']) / long_data['close price (call)']) * 100).round(2)
        long_data['breakeven price (call)'] = long_data['breakeven price (call)'].round(2)

        long_data = long_data[long_target > long_data['breakeven price (call)']]
        long_positions = long_data.sort_values(by='RoR (call)', ascending=False).set_index('contract symbol (call)')

    if short_target is not None:
        short_data = option_data.copy()
        
        short_data = short_data[[ 
            'symbol underlying', 'remained day', 'strike price', 'close price (underlying)', 'close price (underlying) %', 'RoR (underlying) short', 
            'contract symbol (put)', 'contract name (put)', 'value (put)', 'notional value (put)', 'open interest (put)', 
            'close price (put)', 'close price (put) %', 'status (put)', 'detailed_status (put)',
            'implied volatility (put)', 'Black-Scholes value (put)', 'valuation status (put)',
            'delta (put)', 'gamma (put)', 'theta (put)', 'vega (put)', 'rho (put)'
        ]].copy()

        short_data['breakeven price (put)'] = short_data['strike price'] - short_data['close price (put)']
        short_data['RoR (put)'] = (((short_target - short_data['breakeven price (put)']) / short_data['close price (put)']) * 100).round(2)
        short_data['breakeven price (put)'] = short_data['breakeven price (put)'].round(2)

        short_data = short_data[short_target < short_data['breakeven price (put)']]
        short_positions = short_data.sort_values(by='RoR (put)', ascending=True).set_index('contract symbol (put)')

    return long_positions, short_positions