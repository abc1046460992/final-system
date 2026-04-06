import sys

with open('main_100_percent_v3.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_code = '''    # --- get_academic_progress ---
    def get_academic_progress(self):
        # ========================================
        from datetime import date, timedelta
        import pandas as pd
        try:
            df = normalize_calendar_columns(self.df_calendar).copy()
            if df.empty:
                return {'year_total': 0, 'year_curr': 0, 'year_pct': 0, 'terms': []}
            
            df["_d"] = df["التاريخ الميلادي"].apply(safe_parse_date)
            df = df[df["_d"].notna()]
            if df.empty:
                return {'year_total': 0, 'year_curr': 0, 'year_pct': 0, 'terms': []}
                
            today = date.today()
            df["composite_week"] = df["الفصل الدراسي"].astype(str) + "_" + df["الأسبوع"].astype(str)
            unique_weeks = df.drop_duplicates(subset=["composite_week"])
            total_year_weeks = len(unique_weeks)
            passed_year_weeks = len(unique_weeks[unique_weeks["_d"] <= today])
            year_pct = int(passed_year_weeks / total_year_weeks * 100) if total_year_weeks > 0 else 0
            
            terms_data = []
            term_names = df["الفصل الدراسي"].unique()
            term_order = []
            for t in term_names:
                first_dt = df[df["الفصل الدراسي"] == t]["_d"].min()
                term_order.append((t, first_dt))
                
            term_order.sort(key=lambda x: x[1])
            current_term_name = self.get_day_status(today).get("term", "")
            
            for t_name, _ in term_order:
                clean_name = normalize_arabic(str(t_name))
                if "اجاز" in clean_name:
                    continue
                    
                t_df = df[df["الفصل الدراسي"] == t_name]
                t_weeks = t_df["الأسبوع"].unique()
                t_total = len(t_weeks)
                t_passed_df = t_df[t_df["_d"] <= today]
                t_passed_count = len(t_passed_df["الأسبوع"].unique())
                t_pct = int(t_passed_count / t_total * 100) if t_total > 0 else 0
                
                t_start_day = t_df["_d"].min()
                t_last_day = t_df["_d"].max()
                t_days_left = (t_last_day - today).days if (pd.notna(t_last_day) and t_last_day >= today) else 0
                
                is_curr = (normalize_arabic(t_name) == normalize_arabic(current_term_name))
                if not is_curr and pd.notna(t_start_day) and pd.notna(t_last_day):
                    extended_end = t_last_day + timedelta(days=25) # Guess current term if close
                    if t_start_day <= today <= extended_end:
                        is_curr = True
                        
                terms_data.append({
                    'name': t_name,
                    'total': t_total,
                    'curr': t_passed_count,
                    'pct': t_pct,
                    'days_left': t_days_left,
                    'is_current': is_curr
                })
                
            return {
                'year_total': total_year_weeks,
                'year_curr': passed_year_weeks,
                'year_pct': year_pct,
                'terms': terms_data
            }
        except Exception:
            return {'year_total': 0, 'year_curr': 0, 'year_pct': 0, 'terms': []}
            
'''

start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if line.startswith('    # --- get_academic_progress ---'):
        start_idx = i
    if start_idx != -1 and line.startswith('    # --- filter_calendar ---'):
        end_idx = i
        break

if start_idx != -1 and end_idx != -1:
    del lines[start_idx:end_idx]
    lines.insert(start_idx, new_code)
    with open('main_100_percent_v3.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Patched get_academic_progress")
else:
    print("Could not find get_academic_progress block")
