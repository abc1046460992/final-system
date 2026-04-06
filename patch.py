import io, os
from datetime import datetime

with io.open('main_100_percent_v3.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def insert_methods():
    for i, line in enumerate(lines):
        if 'def get_employee_role(self, emp_name=None):' in line:
            return i
    return -1

insert_idx = insert_methods()
if insert_idx != -1:
    new_methods = '''    # --- load_task_history ---
    def load_task_history(self):
        import json
        fpath = data_path("employee_task_history.json")
        if not os.path.exists(fpath): return []
        try:
            with open(fpath, "r", encoding="utf-8") as f: return json.load(f)
        except: return []

    # --- save_task_history ---
    def save_task_history(self, history_list=None):
        import json
        fpath = data_path("employee_task_history.json")
        try:
            with open(fpath, "w", encoding="utf-8") as f: json.dump(history_list, f, ensure_ascii=False)
            return True
        except: return False

    # --- log_role_assignment ---
    def log_role_assignment(self, emp_name=None, task_name=None, action="add"):
        history = self.load_task_history()
        today_str = datetime.now().strftime("%Y-%m-%d")
        
        if action == "add":
            active_exists = any((h for h in history if h.get("employee") == emp_name and h.get("task") == task_name and h.get("status") == " Õ  «·⁄„·"))
            if not active_exists:
                history.append({
                    "employee": emp_name,
                    "task": task_name,
                    "start_date": today_str,
                    "end_date": "",
                    "status": " Õ  «·⁄„·"
                })
        elif action == "remove":
            for h in history:
                if h.get("employee") == emp_name and h.get("task") == task_name and h.get("status") == " Õ  «·⁄„·":
                    h["end_date"] = today_str
                    h["status"] = "„‰ ÂÌ"
        self.save_task_history(history)

    # ========================================

'''
    lines.insert(insert_idx, new_methods)
    with io.open('main_100_percent_v3.py', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    print("Methods added successfully")
else:
    print("Hook point not found")
