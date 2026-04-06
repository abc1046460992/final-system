import pandas as pd
import math

try:
    df = pd.read_excel('بيانات_الطلاب.xlsx')
    col_name = 'رقم جوال الطالب'
    
    if col_name not in df.columns:
        print(f"Column '{col_name}' not found!")
    else:
        total = len(df)
        phones = df[col_name].tolist()
        
        valid_966 = 0
        starts_05 = 0
        starts_5 = 0
        empty_count = 0
        invalid = []
        
        for p in phones:
            if pd.isna(p) or str(p).strip() == '':
                empty_count += 1
                continue
                
            p_str = str(int(p)) if isinstance(p, float) and not math.isnan(p) else str(p).strip()
            
            # check ideal format
            if p_str.startswith('9665') and len(p_str) == 12:
                valid_966 += 1
            elif p_str.startswith('05') and len(p_str) == 10:
                starts_05 += 1
            elif p_str.startswith('5') and len(p_str) == 9:
                starts_5 += 1
            else:
                invalid.append(p_str)

        print(f"--- Phone Number Analysis ---")
        print(f"Total Rows: {total}")
        print(f"Empty/Missing: {empty_count}")
        print(f"Ideal Format (9665xxxxxxxx): {valid_966}")
        print(f"Starts with 05 (05xxxxxxxx): {starts_05} -> Needs '966' prepended, drop '0'")
        print(f"Starts with 5 (5xxxxxxxx): {starts_5} -> Needs '966' prepended")
        print(f"Invalid/Unknown Format: {len(invalid)}")
        if invalid:
            print(f"Sample Invalid: {invalid[:10]}")

except Exception as e:
    print(f"Error: {e}")
