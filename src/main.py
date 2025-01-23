import pandas as pd
import re
import os
from pathlib import Path
from data.loader import BankDataLoader
import config
from datetime import datetime, timedelta
from analysis.reports import rolling_12_month_average, monthly_totals, list_of_categories

loader = BankDataLoader(config.DATA_DIRS)
data = loader.load_statements()
# Temp: Filter out transactions before 2024_02
data = data[data['Date'] >= '2023-02-01']
loader.dump_intermediate(data, 'intermediate.csv')





monthly_totals(data)

rolling_12_month_average(data)

# categories = list_of_categories(data)
# print(categories)