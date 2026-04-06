import os
import sys
from datetime import datetime, timedelta
sys.path.append(os.getcwd())
try:
    from main_100_percent_v3 import DataModel, normalize_calendar_columns, safe_parse_date, tidy, normalize_arabic
    model = DataModel()
    
    df = normalize_calendar_columns(model.df_calendar).copy()
    df['_d'] = df['التاريخ الميلادي'].apply(safe_parse_date)
    df = df[df['_d'].notna()].sort_values('_d')
    df = df[df['الأسبوع'].astype(str) != '17']
    keywords = ['رمضان', 'اضحى', 'فطر', 'تاسيس', 'وطني', 'فصل', 'عطل', 'اجاز', 'عيد', 'يوم']
    
    holidays_list = []
    
    for _, r in df.iterrows():
        note = tidy(r.get('الملاحظات', ''))
        n_norm = normalize_arabic(note)
        is_major = any((k in n_norm for k in keywords))
        if is_major and len(n_norm) > 2:
            dt = r['_d']
            hij = tidy(r.get('التاريخ الهجري', ''))
            
            merged = False
            for h in holidays_list:
                # Check if it's within 6 days (to cross weekends)
                if 0 <= (dt - h['end_dt']).days <= 6:
                    # check for common keywords to prevent merging totally different holidays
                    w1 = set(n_norm.split()) - set(['اجازة', 'بداية', 'نهاية'])
                    w2 = set(normalize_arabic(h['name']).split()) - set(['اجازة', 'بداية', 'نهاية'])
                    
                    if w1.intersection(w2) or ('مطول' in n_norm and 'مطول' in normalize_arabic(h['name'])):
                        h['end_dt'] = dt
                        h['end_h'] = hij
                        if 'بداية' in h['name'] and 'بداية' not in note:
                            h['name'] = note
                        merged = True
                        break
            
            if not merged:
                holidays_list.append({
                    'name': note,
                    'start_dt': dt,
                    'end_dt': dt,
                    'start_h': hij,
                    'end_h': hij
                })
                
    for h in holidays_list:
        h['duration'] = (h['end_dt'] - h['start_dt']).days + 1
        print(f"{h['name']} | {h['start_dt']} to {h['end_dt']} ({h['duration']} days)")

except Exception as e:
    import traceback
    traceback.print_exc()
