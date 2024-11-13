import pandas as pd
import numpy as np
from statsmodels.tsa.filters.hp_filter import hpfilter
import matplotlib.pyplot as plt

# Load the data
# Load datasets
gdp_hk = pd.read_csv('HK GDP.csv', parse_dates=['Date'], index_col='Date')
export_hk = pd.read_csv('HK EXPORTS.csv', parse_dates=['Date'], index_col='Date')
gdp_us = pd.read_csv('US GDP.csv', parse_dates=['Date'], index_col='Date')
export_us = pd.read_csv('US EXPORTS.csv', parse_dates=['Date'], index_col='Date')

# Check start dates
print("Start dates of individual datasets:")
print("Hong Kong GDP start date:", gdp_hk.index.min())
print("Hong Kong Export start date:", export_hk.index.min())
print("U.S. GDP start date:", gdp_us.index.min())
print("U.S. Export start date:", export_us.index.min())

# Determine the latest start date to align all data
latest_start_date = max(gdp_hk.index.min(), export_hk.index.min(), gdp_us.index.min(), export_us.index.min())
print("\nAligning data to start from:", latest_start_date)

# Trim each dataset to start from the latest start date
gdp_hk = gdp_hk[gdp_hk.index >= latest_start_date]
export_hk = export_hk[export_hk.index >= latest_start_date]
gdp_us = gdp_us[gdp_us.index >= latest_start_date]
export_us = export_us[export_us.index >= latest_start_date]

# Merge datasets on the 'Date' index
data = gdp_hk.join([export_hk, gdp_us, export_us], how='inner')

# Rename columns for clarity
data.columns = ['GDP_HK', 'Export_HK', 'GDP_US', 'Export_US']

# Save to CSV with descriptive filename
data.to_csv('gdp_export_hk_us_quarterly.csv')
print("\nData cleaned, aligned to the latest start date, and saved as 'gdp_export_hk_us_quarterly.csv'")

# Assuming your CSV file has columns 'Date', 'GDP_HK', 'Export_HK', 'GDP_US', 'Export_US'
data = pd.read_csv('gdp_export_hk_us_quarterly.csv', parse_dates=['Date'], index_col='Date')

# Take logs of GDP and export data for both Hong Kong and the U.S.
data['log_GDP_HK'] = np.log(data['GDP_HK'])
data['log_Export_HK'] = np.log(data['Export_HK'])
data['log_GDP_US'] = np.log(data['GDP_US'])
data['log_Export_US'] = np.log(data['Export_US'])

# Applying HP filter to log-transformed data
cycle_log_GDP_HK, trend_log_GDP_HK = hpfilter(data['log_GDP_HK'], lamb=1600)
cycle_log_Export_HK, trend_log_Export_HK = hpfilter(data['log_Export_HK'], lamb=1600)
cycle_log_GDP_US, trend_log_GDP_US = hpfilter(data['log_GDP_US'], lamb=1600)
cycle_log_Export_US, trend_log_Export_US = hpfilter(data['log_Export_US'], lamb=1600)

# Adding HP-filtered cyclical components to the DataFrame
data['cycle_log_GDP_HK'] = cycle_log_GDP_HK
data['cycle_log_Export_HK'] = cycle_log_Export_HK
data['cycle_log_GDP_US'] = cycle_log_GDP_US
data['cycle_log_Export_US'] = cycle_log_Export_US

plt.figure()
plt.plot(data.index, data['cycle_log_GDP_HK'], label='GDP')
plt.plot(data.index, data['cycle_log_Export_HK'], label='Export')
plt.title("HK HP flitered log real Data")
plt.xlabel('Date')
plt.legend()
plt.show()

plt.plot(data.index, data['cycle_log_GDP_US'], label='GDP')
plt.plot(data.index, data['cycle_log_Export_US'], label='Export')
plt.title("US HP flitered log real Data")
plt.xlabel('Date')
plt.legend()
plt.show()

plt.plot(data.index, data['cycle_log_GDP_HK'], label='HK')
plt.plot(data.index, data['cycle_log_GDP_US'], label='US')
plt.title('HK & US HP flitered log real GDP')
plt.xlabel('Date')
plt.legend()
plt.show()

# Correlation for Hong Kong
corr_HK = data[['cycle_log_GDP_HK', 'cycle_log_Export_HK']].corr()
print("Correlation between HP-filtered log GDP and log Export for Hong Kong:") 
print(corr_HK)

# Correlation for the U.S.
corr_US = data[['cycle_log_GDP_US', 'cycle_log_Export_US']].corr()
print("Correlation between HP-filtered log GDP and log Export for the U.S.:")
print(corr_US)

# Correlation between HP-filtered log GDP of Hong Kong and the U.S.
corr_GDP_HK_US = data[['cycle_log_GDP_HK', 'cycle_log_GDP_US']].corr() 
print("Correlation between HP-filtered log GDP in Hong Kong and U.S.:") 
print(corr_GDP_HK_US)

