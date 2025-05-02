import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import statsmodels.api as sm

df = pd.read_csv('your-fee-history-here.csv')
df['Symbol'] = df['Symbol'].fillna('USDT')
print(df.isnull().sum())

funding_fee_data = df[df['type'] == 'FUNDING_FEE']

def detect_outliers(series):
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return series[(series < lower_bound) | (series > upper_bound)]

#Date Formatter
funding_fee_data['Date(UTC)'] = pd.to_datetime(funding_fee_data['Date(UTC)'], utc=True)

#Calculate Rolling Mean
funding_fee_data['21_day_avg'] = funding_fee_data['Amount'].rolling(window=21, min_periods=21).mean()
funding_fee_data['50_day_avg'] = funding_fee_data['Amount'].rolling(window=50, min_periods=50).mean()
funding_fee_data['200_day_avg'] = funding_fee_data['Amount'].rolling(window=200, min_periods=200).mean()

#Plot Graph
plt.figure(figsize=(12, 6))
sns.lineplot(x='Date(UTC)', y='21_day_avg', data=funding_fee_data, label='21-Day Rolling Mean', color='green')
sns.lineplot(x='Date(UTC)', y='50_day_avg', data=funding_fee_data, label='50-Day Rolling Mean', color='orange')
sns.lineplot(x='Date(UTC)', y='200_day_avg', data=funding_fee_data, label='200-Day Rolling Mean', color='red')

#Context
event_date_1 = pd.to_datetime('2024-08-05')
event_date_2 = pd.to_datetime('2024-09-06')
event_date_3 = pd.to_datetime('2024-12-17')

plt.axvline(x=event_date_1, color='r', linestyle='--', label='Q3 Crash')
plt.axvspan(event_date_2, event_date_3, color='blue', alpha=0.3, 
label='ATH run')

#Layout
plt.title('Year-to-date Funding Fee Rolling Average', fontsize=16)
plt.xlabel('Date(UTC)')
plt.ylabel('Amount(USD)')
plt.legend(title='Rolling Averages')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval = 30))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
