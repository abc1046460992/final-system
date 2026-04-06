import sys

with open('main_100_percent_v3.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_code = '''def normalize_calendar_columns(df=None):
    # ========================================
    import pandas as pd
    if df is None or df.empty:
        return pd.DataFrame(columns=['الفصل الدراسي', 'الأسبوع', 'اليوم', 'التاريخ الهجري', 'التاريخ الميلادي', 'الملاحظات'])
    mapping = {}
    for col in df.columns:
        c = str(col).strip()
        c_low = c.lower()
        if "فصل" in c:
            mapping[col] = "الفصل الدراسي"
        elif "سبوع" in c:
            mapping[col] = "الأسبوع"
        elif "يوم" in c or "اليوم" == c:
            mapping[col] = "اليوم"
        elif "ميلاد" in c or "m" in c_low or c_low == "م":
            mapping[col] = "التاريخ الميلادي"
        elif "هجر" in c or "h" in c_low or "هـ" in c_low:
            mapping[col] = "التاريخ الهجري"
        elif "ملاحظ" in c:
            mapping[col] = "الملاحظات"
            
    df = df.rename(columns=mapping)
    needed_cols = ['الفصل الدراسي', 'الأسبوع', 'اليوم', 'التاريخ الهجري', 'التاريخ الميلادي', 'الملاحظات']
    for needed in needed_cols:
        if needed not in df.columns:
            df[needed] = ""
            
    return df[needed_cols].copy()

# ========================================
'''

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.startswith('def normalize_calendar_columns(df=None):'):
        start_idx = i
    if start_idx != -1 and line.startswith('# --- parse_teacher_cell ---'):
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    del lines[start_idx:end_idx]
    lines.insert(start_idx, new_code)
    with open('main_100_percent_v3.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Patched normalize_calendar_columns")
else:
    print("Block not found")
