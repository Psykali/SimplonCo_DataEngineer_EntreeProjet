# timeseries_analysis.py
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

# Load data
df = pd.read_sql('''
  SELECT sale_date, SUM(amount) as daily_revenue 
  FROM sales GROUP BY sale_date ORDER BY sale_date
''', conn)

# Convert to time series
df['sale_date'] = pd.to_datetime(df['sale_date'])
df.set_index('sale_date', inplace=True)

# ARIMA model for forecasting
model = ARIMA(df, order=(5,1,0))
model_fit = model.fit()
forecast = model_fit.forecast(steps=7)  # 7-day forecast

print("🔮 Next Week Forecast:")
print(forecast)
