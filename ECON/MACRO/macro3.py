!pip install pandas statsmodels

import pandas as pd
import numpy as np
from statsmodels.tsa.filters.hp_filter import hpfilter

# Load the data
# Assuming your CSV file has columns 'Date', 'GDP_HK', 'Export_HK', 'GDP_US', 'Export_US'
data = pd.read_csv('path_to_your_data_file.csv', parse_dates=['Date'], index_col='Date')

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

# Correlation for Hong Kong
corr_HK = data[['cycle_log_GDP_HK', 'cycle_log_Export_HK']].corr().iloc[0, 1]
print(f"Correlation between HP-filtered log GDP and log Export for Hong Kong: {corr_HK}")

# Correlation for the U.S.
corr_US = data[['cycle_log_GDP_US', 'cycle_log_Export_US']].corr().iloc[0, 1]
print(f"Correlation between HP-filtered log GDP and log Export for the U.S.: {corr_US}")

# Correlation between HP-filtered log GDP of Hong Kong and the U.S.
corr_GDP_HK_US = data[['cycle_log_GDP_HK', 'cycle_log_GDP_US']].corr().iloc[0, 1]
print(f"Correlation between HP-filtered log GDP in Hong Kong and U.S.: {corr_GDP_HK_US}")

