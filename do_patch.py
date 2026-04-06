import sys

with open('main_100_percent_v3.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_open_details = '''            def open_details(evt=None):
                sel = tv.selection()
                if not sel:
                    if evt is None:
                        messagebox.showwarning("تنبيه", "الرجاء اختيار طالب أولاً.")
                    return
                idx = int(sel[0])
                student_data = self.m.get_student_full(idx)
                student_name = tidy(student_data.get("الاسم", ""))
                win = tk.Toplevel(self)
                win.title(f"ملف الطالب: {student_name}")
                win.geometry("900x700")
                win.grab_set()
                top_frame = tk.Frame(win, bg=COLOR_PANEL, height=80)
                top_frame.pack(fill="x", padx=10, pady=10)
                ttk.Label(top_frame, text=f"📂 ملف الطالب: {student_name}", font=('Segoe UI', 16, 'bold'),
                  foreground=COLOR_ACCENT).pack(side="right", padx=20, pady=10)
                notebook = ttk.Notebook(win)
                notebook.pack(fill="both", expand=True, padx=10, pady=5)
                
                # --- TAB 1: Schedule ---
                tab_schedule = tk.Frame(notebook, bg=COLOR_BG)
                notebook.add(tab_schedule, text="  📅 حصص الطالب  ")

                f_filter = tk.Frame(tab_schedule, bg=COLOR_BG)
                f_filter.pack(fill="x", padx=10, pady=10)
                v_day = tk.StringVar(value="الكل")
                v_period = tk.StringVar(value="الكل")
                tk.Label(f_filter, text="تصفية حسب اليوم:", bg=COLOR_BG).pack(side="right", padx=5)
                cb_day = ttk.Combobox(f_filter, values=(["الكل"] + DAYS), textvariable=v_day, state="readonly", width=12)
                cb_day.pack(side="right", padx=5)
                tk.Label(f_filter, text="الحصة:", bg=COLOR_BG).pack(side="right", padx=5)
                cb_period = ttk.Combobox(f_filter, values=(["الكل"] + [str(i) for i in range(1, 8)]), textvariable=v_period, state="readonly", width=8)
                cb_period.pack(side="right", padx=5)
                s_class = tidy(student_data.get("الصف", ""))
                s_section = tidy(student_data.get("الشعبة", ""))
                raw_results, _, _ = self.m.find_student_schedule(student_name, s_class, s_section)
                cols = ['اليوم', 'الحصة', 'من', 'إلى', 'المعلم', 'المادة/الصف']
                tv_sch = ttk.Treeview(tab_schedule, columns=cols, show="headings", height=12)
                for c in cols:
                    tv_sch.heading(c, text=c)
                    width = 100
                    if c == "المادة/الصف":
                        width = 200
                    tv_sch.column(c, anchor="center", width=width)
                vsb_sch = ttk.Scrollbar(tab_schedule, orient="vertical", command=tv_sch.yview)
                tv_sch.configure(yscrollcommand=vsb_sch.set)
                vsb_sch.pack(side="left", fill="y")
                tv_sch.pack(side="right", fill="both", expand=True)

                def apply_filters(*args, **kwargs):
                    for item in tv_sch.get_children():
                        tv_sch.delete(item)
                    d_filter = v_day.get()
                    p_filter = v_period.get()
                    for r in raw_results:
                        if d_filter != "الكل" and r.get("اليوم") != d_filter: continue
                        if p_filter != "الكل" and str(r.get("الحصة")) != p_filter: continue
                        tv_sch.insert("", "end", values=[r.get(c, "") for c in cols])

                cb_day.bind("<<ComboboxSelected>>", apply_filters)
                cb_period.bind("<<ComboboxSelected>>", apply_filters)
                cb_day.bind("<Return>", apply_filters)
                cb_period.bind("<Return>", apply_filters)
                tk.Button(f_filter, text="🔍 بحث / تصفية", command=apply_filters, bg="#eee").pack(side="right", padx=5)

                def do_export():
                    if not raw_results:
                        messagebox.showinfo("تنبيه", "لا يوجد جدول لتصديره.")
                        return
                    filtered = []
                    d_filter = v_day.get()
                    p_filter = v_period.get()
                    for r in raw_results:
                        if d_filter != "الكل" and r.get("اليوم") != d_filter: continue
                        if p_filter != "الكل" and str(r.get("الحصة")) != p_filter: continue
                        filtered.append(r)
                    if not filtered:
                        messagebox.showinfo("تنبيه", "الجدول فارغ (حسب التصفية الحالية).")
                        return
                    try:
                        import xlsxwriter
                        import os
                        fname = f"جدول_الطالب_{student_name}.xlsx"
                        fpath = os.path.abspath(fname)
                        wb = xlsxwriter.Workbook(fpath)
                        ws = wb.add_worksheet("الجدول")
                        ws.right_to_left()
                        fmt_head = wb.add_format({'bold': True, 'bg_color': '#2e7d32', 'font_color': 'white', 'border': 1, 'align': 'center'})
                        fmt_cell = wb.add_format({'border':1,  'align':"center"})
                        for i, c in enumerate(cols):
                            ws.write(0, i, c, fmt_head)
                        for r_i, d in enumerate(filtered):
                            for c_i, col in enumerate(cols):
                                ws.write(r_i + 1, c_i, d.get(col, ""), fmt_cell)
                        wb.close()
                        os.startfile(fpath)
                        messagebox.showinfo("تم", f"تم تصدير الجدول بنجاح:\\n{fname}")
                    except Exception as ex:
                        messagebox.showerror("خطأ", f"فشل التصدير: {ex}")

                tk.Button(f_filter, text="📥 تصدير الجدول (Excel)", command=do_export, bg=COLOR_XLSX,
                  fg="white", font=('Segoe UI', 9, 'bold')).pack(side="left", padx=10)
                apply_filters()

                # --- TAB 2: Personal Data ---
                tab_personal = tk.Frame(notebook, bg=COLOR_BG)
                notebook.add(tab_personal, text="  👤 بيانات خاصة  ")
                canvas = tk.Canvas(tab_personal, bg=COLOR_BG)
                scrollbar = ttk.Scrollbar(tab_personal, orient="vertical", command=canvas.yview)
                scrollable_frame = ttk.Frame(canvas)
                scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
                canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
                canvas.configure(yscrollcommand=scrollbar.set)
                canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
                scrollbar.pack(side="right", fill="y")
                
                frm_personal = scrollable_frame
                entries = {}
                row_i = 0
                for key in sorted(student_data.keys()):
                    ttk.Label(frm_personal, text=(key + ":")).grid(row=row_i, column=0, sticky="e", padx=6, pady=6)
                    ent = ttk.Entry(frm_personal, width=40)
                    ent.grid(row=row_i, column=1, sticky="w", padx=6, pady=6)
                    ent.insert(0, tidy(student_data.get(key, "")))
                    entries[key] = ent
                    row_i += 1

                def save_personal_data():
                    updated = {k: tidy(e.get()) for k, e in entries.items()}
                    self.m.update_student_full(idx, updated)
                    messagebox.showinfo("تم", "تم حفظ البيانات الخاصة بنجاح.")
                    try:
                        reload_students()
                    except:
                        pass

                btn_save = tk.Button(frm_personal, text="💾 حفظ التعديلات", command=save_personal_data, bg=COLOR_ACCENT, fg="white", font=('Segoe UI', 10, 'bold'))
                if not self.admin_mode:
                    btn_save.config(state="disabled", bg="#ccc")
                btn_save.grid(row=row_i, column=0, columnspan=2, pady=20, sticky="ew")
                
                wm_bar = tk.Frame(win, bg=COLOR_PANEL)
                wm_bar.pack(side="bottom", fill="x")
                final_res, _, _ = self.m.find_student_schedule(student_name)
                tk.Button(wm_bar, text="📄 إذن خروج (Word)", bg=COLOR_BTN, fg="white", command=(lambda: self.open_exit_permit_dialog(student_name, final_res))).pack(side="right", padx=10, pady=10)
                tk.Button(wm_bar, text="⬇️ تصدير الجدول (Excel)", bg=COLOR_XLSX, fg="white", command=(lambda: self.export_student_schedule_excel(student_name, final_res))).pack(side="right", padx=10, pady=10)
\n'''

del lines[8897:9336]
lines[8728:8895] = [new_open_details]

with open('main_100_percent_v3.py', 'w', encoding='utf-8') as f:
    f.writelines(lines)
