import sys
import codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout.detach())
sys.path.append('.')

try:
    from main_100_percent_v3 import DataModel, normalize_calendar_columns

    m = DataModel()
    print("df_calendar type:", type(m.df_calendar))
    if hasattr(m, 'df_calendar') and m.df_calendar is not None:
        print("df_calendar count:", len(m.df_calendar))
        
    res = m.get_days_until_next_holiday()
    print("vacation result:", res)
    
    prog = m.get_academic_progress()
    print("progress result:", prog)
except Exception as e:
    import traceback
    traceback.print_exc()
