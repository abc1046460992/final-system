import os

def run():
    target_file = 'main_100_percent_v3.py'
    with open(target_file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_1 = """def define_data_path(relative_path):
    return os.path.join(get_base_path(), relative_path)"""
    new_1 = """def define_data_path(relative_path):
    if relative_path and relative_path.endswith(('.xlsx', '.json')):
        db_folder = os.path.join(get_base_path(), "قاعدة_البيانات")
        if not os.path.exists(db_folder):
            try: os.makedirs(db_folder)
            except: pass
        return os.path.join(db_folder, relative_path)
    return os.path.join(get_base_path(), relative_path)"""
    
    old_2 = """    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    target = os.path.join(base_path, relative_path)"""
    
    new_2 = """    if getattr(sys, "frozen", False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.abspath(".")
    
    if relative_path and relative_path.endswith(('.xlsx', '.json')):
        base_path = os.path.join(base_path, "قاعدة_البيانات")
        if not os.path.exists(base_path):
            try: os.makedirs(base_path)
            except: pass

    target = os.path.join(base_path, relative_path)"""

    old_3 = """                # 5. Copy Data Files
                files_to_copy = [f for f in os.listdir(os.getcwd()) if f.endswith(('.xlsx', '.json', '.png', '.docx'))]
                for f in files_to_copy:
                    src = os.path.join(os.getcwd(), f)
                    dst = os.path.join(delivery_dir, f)
                    if os.path.isfile(src) and src != dst:
                        shutil.copy2(src, dst)
                        self.after(0, lambda f=f: update_status("", f">>> تم نسخ: {f}"))"""
                        
    new_3 = """                # 5. Copy Data Files Folder
                src_db = os.path.join(os.getcwd(), "قاعدة_البيانات")
                dst_db = os.path.join(delivery_dir, "قاعدة_البيانات")
                if os.path.exists(src_db):
                    from shutil import copytree
                    try:
                        copytree(src_db, dst_db, dirs_exist_ok=True)
                        self.after(0, lambda: update_status("", f">>> تم نسخ مجلد قاعدة البيانات بنجاح"))
                    except Exception as e:
                        self.after(0, lambda ex=e: update_status("", f"❌ بعض الأخطاء أثناء نسخ البيانات: {ex}"))"""

    if old_1 in content:
        content = content.replace(old_1, new_1)
        print("Success: define_data_path updated.")
    else:
        print("Error: Could not find old_1")

    if old_2 in content:
        content = content.replace(old_2, new_2)
        print("Success: data_path updated.")
    else:
        print("Error: Could not find old_2")

    if old_3 in content:
        content = content.replace(old_3, new_3)
        print("Success: deploy logic updated.")
    else:
        print("Error: Could not find old_3")

    with open(target_file, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == '__main__':
    run()
