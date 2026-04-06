import sys

with open('main_100_percent_v3.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    # --- get_current_active_period ---
    def get_current_active_period(self):
        # ========================================
        # [DECOMPILATION FAILED]: 



        # ========================================
        return None

    # --- get_current_active_period_parse_t ---
    def get_current_active_period_parse_t(t_str=None):
        # ========================================
        # [DECOMPILATION FAILED]: 



        # ========================================
        return None'''

new_code = '''    # --- get_current_active_period ---
    def get_current_active_period(self):
        # ========================================
        from datetime import datetime
        try:
            if getattr(self, "df_timings", None) is None or self.df_timings.empty:
                return ("--", "Out", 0)
                
            def parse_t(t_str):
                try:
                    s = str(t_str).replace("ص", "").replace("م", "").strip()
                    h, m = map(int, s.split(":"))
                    return h, m
                except Exception:
                    return None
                    
            now = datetime.now()
            t_now_dt = now
            min_dt = None
            max_dt = None
            
            for _, row in self.df_timings.iterrows():
                name = str(row.get("الحصة", ""))
                from_t = parse_t(row.get("من", ""))
                to_t = parse_t(row.get("إلى", ""))
                if from_t and to_t:
                    start_dt = now.replace(hour=from_t[0], minute=from_t[1], second=0, microsecond=0)
                    end_dt = now.replace(hour=to_t[0], minute=to_t[1], second=0, microsecond=0)
                    
                    if min_dt is None or start_dt < min_dt: min_dt = start_dt
                    if max_dt is None or end_dt > max_dt: max_dt = end_dt
                    
                    if start_dt <= t_now_dt <= end_dt:
                        rem_minutes = max(0, int((end_dt - t_now_dt).total_seconds() / 60))
                        return (name, "Active", rem_minutes)
                        
            if min_dt and max_dt:
                if t_now_dt < min_dt or t_now_dt > max_dt:
                    return ("--", "Out", 0)
            return ("--", "Wait", 0)
        except Exception:
            return ("--", "Out", 0)'''

if target in text:
    with open('main_100_percent_v3.py', 'w', encoding='utf-8') as f:
        f.write(text.replace(target, new_code))
    print("Patched successfully!")
else:
    print("Target not found.")

