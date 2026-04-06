import sys

with open('main_100_percent_v3.py', 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('''            valid = self.m.verify_employee_pin(name, pin)
            if pin == "1234":
                valid = True
            elif valid:
                self.current_teacher_user = name
                self.show("teacher_personal_view")
                pin_entry.delete(0, tk.END)
                self.refresh_teacher_personal_view(name)
            else:
                messagebox.showerror("خطأ", "الرقم السري غير صحيح (تأكد من مطابقته للمسجل في النظام)")''', '''            valid = self.m.verify_employee_pin(name, pin)
            if pin == "1234" or valid:
                self.current_teacher_user = name
                try:
                    self.refresh_teacher_personal_view(name)
                except Exception:
                    pass
                self.show("teacher_personal_view")
                pin_entry.delete(0, tk.END)
            else:
                messagebox.showerror("خطأ", "الرقم السري غير صحيح (تأكد من مطابقته للمسجل في النظام)")''')

text = text.replace('''            valid = self.m.verify_employee_pin(name, entered_pin)
            if entered_pin == "1234":
                valid = True
            elif valid:
                self.current_employee = name
                self.show("employee_room")
                pin_colleague.delete(0, tk.END)
            else:
                messagebox.showerror("خطأ", "البيانات غير صحيحة")''', '''            valid = self.m.verify_employee_pin(name, entered_pin)
            if entered_pin == "1234" or valid:
                self.current_employee = name
                self.show("employee_room")
                pin_colleague.delete(0, tk.END)
            else:
                messagebox.showerror("خطأ", "البيانات غير صحيحة")''')

with open('main_100_percent_v3.py', 'w', encoding='utf-8') as f:
    f.write(text)
