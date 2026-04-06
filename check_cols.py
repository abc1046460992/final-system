import pandas as pd
import json

files = ['المعلمين.xlsx', 'الإداريين.xlsx', 'بيانات_الطلاب.xlsx']
result = {}

for f in files:
    try:
        df = pd.read_excel(f)
        cols = list(df.columns)
        # Find which column might contain phone numbers by looking at first 5 rows
        sample_phones = []
        possible_phone_cols = []
        for c in cols:
            if 'رقم' in str(c) or 'جوال' in str(c) or 'هاتف' in str(c) or 'تواصل' in str(c):
                possible_phone_cols.append(str(c))
                # Add sample if it's numeric/starts with 05 or 966
                sample = df[c].dropna().head(3).tolist()
                sample_phones.append({str(c): sample})
        
        result[f] = {
            "all_columns": [str(c) for c in cols],
            "phone_columns": possible_phone_cols,
            "samples": sample_phones,
            "total_rows": len(df)
        }
    except Exception as e:
        result[f] = {"error": str(e)}

with open('scan_result.json', 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=4)
