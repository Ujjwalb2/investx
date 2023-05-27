import pandas as pd
import time
import datetime
import matplotlib.pyplot as plt

period1 = int(time.mktime(datetime.datetime(2020, 12, 1, 23, 59).timetuple()))
period2 = int(time.mktime(datetime.datetime(2023, 5, 26, 23, 59).timetuple()))
interval = '1d'
url = f'https://query1.finance.yahoo.com/v7/finance/download/%5ENSEI?period1={period1}&period2={period2}&interval={interval}&events=history&includeAdjustedClose=true'
df = pd.read_csv(url)

trend_periods = 10  # Define an appropriate value for trend_periods

for index, row in df.iterrows():
    if row['Low'] != row['High']:
        ac = ((row['Close'] - row['Low']) - (row['High'] - row['Close'])) / (row['High'] - row['Low']) * row['Volume']
    else:
        ac = 0
    df.at[index, 'acc_dist'] = ac

df['acc_dist_ema' + str(trend_periods)] = df['acc_dist'].ewm(ignore_na=False, min_periods=0, com=trend_periods, adjust=True).mean()

# Convert the 'Date' column to datetime format
df['Date'] = pd.to_datetime(df['Date'])

plt.plot(df['Date'], df.iloc[:, -2], label='Accumulation/Distribution')
# Adding labels and title to the plot
plt.xlabel('Date')
plt.ylabel('Value')
plt.title('Accumulation/Distribution vs. Accumulation/Distribution EMA')

# Rotating the x-axis labels for better visibility (optional)
plt.xticks(rotation=45)

# Adding a legend
plt.legend()

# Displaying the plot
plt.show()
