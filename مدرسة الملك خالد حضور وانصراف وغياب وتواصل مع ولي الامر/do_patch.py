import re

file_path = 'attendance_main.py'
with open(file_path, 'r', encoding='utf-8') as f:
    txt = f.read()

# Remove 'Teachers Management' card
txt = re.sub(r'make_portal_card\(r2, "إدارة المعلمين".*?\n', '', txt)

# Remove 'Export Parents Numbers' card
txt = re.sub(r'make_portal_card\(r3, "تصدير أرقام أولياء الأمور".*?\n', '', txt)

# Remove 'Teachers Login' from sidebar
txt = re.sub(r'self\.sb\("دخول المعلمين.*?\n', '', txt)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(txt)

print("GUI Patched successfully.")
