import pandas as pd
import os

path = os.path.expanduser('~/Documents/نور/الاعدادات/التقويم_الدراسي.xlsx')
print(f"File exists: {os.path.exists(path)}")
if os.path.exists(path):
    df = pd.read_excel(path)
    print("Columns:", list(df.columns))
    print(f"Num rows: {len(df)}")
    print(df.head())
