import sys
sys.path.append('.')
from main_100_percent_v3 import FILE_CALENDAR
import pandas as pd
import os

print(f"Path: {FILE_CALENDAR}")
print(f"File exists: {os.path.exists(FILE_CALENDAR)}")

if os.path.exists(FILE_CALENDAR):
    try:
        df = pd.read_excel(FILE_CALENDAR)
        print("Columns:", list(df.columns))
        print(f"Num rows: {len(df)}")
    except Exception as e:
        print("Error reading:", e)
