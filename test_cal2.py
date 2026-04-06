import sys
sys.path.append('.')
from main_100_percent_v3 import DataModel

m = DataModel()
print(m.df_calendar.head())
print("Empty?", m.df_calendar.empty)
