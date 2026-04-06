import sys

with open('main_100_percent_v3.py', 'r', encoding='utf-8') as f:
    text = f.read()

target = '''    # --- get_current_active_period ---
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
                    
            now = datetime.now()'''

new_code = '''    # --- get_current_active_period ---
    def get_current_active_period(self):
        # ========================================
        from datetime import datetime
        import datetime as dt_module
        try:
            if getattr(self, "df_timings", None) is None or self.df_timings.empty:
                return ("--", "Out", 0)
                
            def parse_t(t_val):
                try:
                    if isinstance(t_val, dt_module.time):
                        return t_val.hour, t_val.minute
                    if isinstance(t_val, dt_module.datetime):
                        return t_val.hour, t_val.minute
                    s = str(t_val).replace("ص", "").replace("م", "").strip()
                    parts = s.split(":")
                    if len(parts) >= 2:
                        return int(parts[0]), int(parts[1])
                    return None
                except Exception:
                    return None
                    
            now = datetime.now()'''

if target in text:
    with open('main_100_percent_v3.py', 'w', encoding='utf-8') as f:
        f.write(text.replace(target, new_code))
    print("Patched robust parse_t successfully!")
else:
    print("Target not found.")

