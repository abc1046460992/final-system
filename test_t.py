import pandas as pd
from datetime import datetime

df = pd.read_excel('المستندات/نور/الاعدادات/توقيت_الحصص.xlsx')
print(df.head())

def parse_t(t_str):
    try:
        h, m = map(int, str(t_str).strip().split(":"))
        return h, m
    except:
        return None

now = datetime.now()
min_dt = None
max_dt = None

for _, row in df.iterrows():
    name = str(row.get("الحصة", ""))
    from_t = parse_t(row.get("من", ""))
    to_t = parse_t(row.get("إلى", ""))
    if from_t and to_t:
        start_dt = now.replace(hour=from_t[0], minute=from_t[1], second=0, microsecond=0)
        end_dt = now.replace(hour=to_t[0], minute=to_t[1], second=0, microsecond=0)
        
        if min_dt is None or start_dt < min_dt: min_dt = start_dt
        if max_dt is None or end_dt > max_dt: max_dt = end_dt
        
        if start_dt <= now <= end_dt:
            rem_minutes = max(0, int((end_dt - now).total_seconds() / 60))
            print((name, "Active", rem_minutes))

if min_dt and max_dt:
    if now < min_dt or now > max_dt:
        print(("--", "Out", 0))
    else:
        print(("--", "Wait", 0))
