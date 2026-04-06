import re
import codecs

with codecs.open('main_100_percent_v3.py', 'r', 'utf-8') as f:
    content = f.read()

new_gui_code = """    # --- send_whatsapp_to_parent ---
    def send_whatsapp_to_parent(self, student_name=None):
        import json
        import threading
        from whatsapp_bot import WhatsAppSenderBot

        # Setup Templates File
        templates_file = data_path("whatsapp_templates.json")
        default_templates = {
            "إشعار غياب": "المكرم ولي أمر الطالب {اسم_الطالب}، نود إشعاركم بغياب ابنكم عن المدرسة اليوم. نأمل منكم الاطمئنان ومراجعتنا.",
            "إشعار تأخير": "المكرم ولي أمر الطالب {اسم_الطالب}، نود إشعاركم بتأخر ابنكم عن الطابور الصباحي اليوم. نأمل منكم حثه على الحضور المبكر."
        }
        if not os.path.exists(templates_file):
            with open(templates_file, "w", encoding="utf-8") as f:
                json.dump(default_templates, f, ensure_ascii=False)
        with open(templates_file, "r", encoding="utf-8") as f:
            saved_templates = json.load(f)

        main_win = tk.Toplevel(self)
        main_win.title("إرسال رسائل واتساب (نظام متقدم)")
        main_win.geometry("900x700")
        main_win.configure(bg="#f4f6f9")
        main_win.grab_set()

        header_frame = tk.Frame(main_win, bg="#128c7e", height=60)
        header_frame.pack(fill="x")
        tk.Label(header_frame, text="💬 إرسال رسائل واتساب (آلي ومتعدد)", font=('Segoe UI', 16, 'bold'), fg="white", bg="#128c7e").pack(pady=15)

        content_frame = tk.Frame(main_win, bg="#f4f6f9")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # LEFT FRAME: Filtering & Selection
        left_frame = tk.LabelFrame(content_frame, text="1️⃣ تحديد المستقبلين", font=('Segoe UI', 12, 'bold'), bg="#ffffff", padx=10, pady=10)
        left_frame.pack(side="right", fill="both", expand=True, padx=5)

        filter_frame = tk.Frame(left_frame, bg="#ffffff")
        filter_frame.pack(fill="x", pady=5)

        tk.Label(filter_frame, text="شريط البحث:", bg="#ffffff", font=('Segoe UI', 10)).grid(row=0, column=2, sticky="e", pady=2)
        search_var = tk.StringVar()
        tk.Entry(filter_frame, textvariable=search_var, font=('Segoe UI', 11), width=20).grid(row=0, column=1, sticky="w", padx=5)

        tk.Label(filter_frame, text="الصف:", bg="#ffffff", font=('Segoe UI', 10)).grid(row=1, column=2, sticky="e", pady=2)
        class_var = tk.StringVar()
        classes = ["الكل", "أول متوسط", "ثاني متوسط", "ثالث متوسط"]
        ttk.Combobox(filter_frame, textvariable=class_var, values=classes, state="readonly", width=18).grid(row=1, column=1, sticky="w", padx=5)
        class_var.set("الكل")

        tk.Label(filter_frame, text="الشعبة:", bg="#ffffff", font=('Segoe UI', 10)).grid(row=2, column=2, sticky="e", pady=2)
        section_var = tk.StringVar()
        sections = ["الكل", "1", "2", "3", "4", "5", "6"]
        ttk.Combobox(filter_frame, textvariable=section_var, values=sections, state="readonly", width=18).grid(row=2, column=1, sticky="w", padx=5)
        section_var.set("الكل")

        # Treeview for multi selection
        columns = ("name", "class", "section", "phone")
        tree_frame = tk.Frame(left_frame, bg="#ffffff")
        tree_frame.pack(fill="both", expand=True, pady=10)
        
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side="left", fill="y")
        
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=tree_scroll.set, selectmode="extended")
        tree.heading("name", text="اسم الطالب")
        tree.heading("class", text="الصف")
        tree.heading("section", text="الشعبة")
        tree.heading("phone", text="رقم ولي الأمر")
        
        tree.column("name", width=150, anchor="e")
        tree.column("class", width=80, anchor="center")
        tree.column("section", width=60, anchor="center")
        tree.column("phone", width=100, anchor="center")
        tree.pack(side="right", fill="both", expand=True)
        tree_scroll.config(command=tree.yview)

        def apply_filter(*args):
            for i in tree.get_children():
                tree.delete(i)
                
            s_text = search_var.get().strip().lower()
            c_filter = class_var.get()
            sec_filter = section_var.get()
            
            try:
                name_col, class_col, section_col = self.m._detect_student_cols()
                phone_col = None
                for col in self.m.df_students.columns:
                    col_lower = str(col).lower()
                    if "جوال" in col_lower:
                        phone_col = col
                        break
                        
                if not phone_col:
                    return

                for idx, row in self.m.df_students.iterrows():
                    name = tidy(row.get(name_col, ""))
                    stu_class = tidy(row.get(class_col, ""))
                    stu_sec = str(row.get(section_col, "")).split('.')[0]
                    phone = tidy(row.get(phone_col, ""))
                    
                    if not name: continue
                    if phone:
                        phone = str(phone).replace(" ", "").replace("-", "")
                        if phone.startswith("0"):
                            phone = "966" + phone[1:]
                        if not phone.startswith("966"):
                            phone = "966" + phone
                            
                    # Filters
                    if s_text and s_text not in name.lower(): continue
                    if c_filter != "الكل" and c_filter not in stu_class: continue
                    if sec_filter != "الكل" and sec_filter != stu_sec: continue
                    
                    tree.insert("", "end", values=(name, stu_class, stu_sec, phone))
            except Exception as e:
                print(e)
                
        search_var.trace("w", apply_filter)
        class_var.trace("w", apply_filter)
        section_var.trace("w", apply_filter)
        
        btn_sel_frame = tk.Frame(left_frame, bg="#ffffff")
        btn_sel_frame.pack(fill="x")
        
        def select_all():
            for item in tree.get_children():
                tree.selection_add(item)
                
        def clear_selection():
            tree.selection_remove(tree.selection())

        tk.Button(btn_sel_frame, text="تحديد الكل", command=select_all, bg="#008CBA", fg="white", font=('Segoe UI', 10)).pack(side="right", padx=2)
        tk.Button(btn_sel_frame, text="إلغاء التحديد", command=clear_selection, bg="#f44336", fg="white", font=('Segoe UI', 10)).pack(side="right", padx=2)
        
        # Populate initial
        apply_filter()

        # RIGHT FRAME: Messages & Execution
        right_frame = tk.Frame(content_frame, bg="#f4f6f9")
        right_frame.pack(side="left", fill="both", expand=True, padx=5)

        msg_frame = tk.LabelFrame(right_frame, text="2️⃣ إعداد الرسالة (الاختصارات)", font=('Segoe UI', 12, 'bold'), bg="#ffffff", padx=10, pady=10)
        msg_frame.pack(fill="x", pady=5)

        tk.Label(msg_frame, text="قوالب جاهزة:", bg="#ffffff", font=('Segoe UI', 10)).grid(row=0, column=1, sticky="e")
        template_var = tk.StringVar()
        template_combo = ttk.Combobox(msg_frame, textvariable=template_var, values=["بدون قالب"] + list(saved_templates.keys()), state="readonly", width=30)
        template_combo.grid(row=0, column=0, sticky="w", pady=5, padx=5)
        template_combo.current(0)

        msg_text = tk.Text(msg_frame, font=('Segoe UI', 11), wrap="word", height=8, width=35)
        msg_text.grid(row=1, column=0, columnspan=2, pady=5)
        msg_text.insert("1.0", "السلام عليكم ورحمة الله وبركاته،\\n")
        
        tk.Label(msg_frame, text="* استخدم {اسم_الطالب} ليكتب اسم كل طالب تلقائياً.", bg="#ffffff", fg="gray", font=('Segoe UI', 9)).grid(row=2, column=0, columnspan=2, sticky="e")

        def on_template_select(e):
            sel = template_var.get()
            if sel in saved_templates:
                msg_text.delete("1.0", tk.END)
                msg_text.insert("1.0", saved_templates[sel])
                
        template_combo.bind("<<ComboboxSelected>>", on_template_select)

        def save_template():
            t_name = tk.simpledialog.askstring("حفظ كقالب", "أدخل اسم القالب الجديد (مثلاً: إشعار درجات):", parent=main_win)
            if t_name:
                saved_templates[t_name] = msg_text.get("1.0", "end-1c").strip()
                with open(templates_file, "w", encoding="utf-8") as f:
                    json.dump(saved_templates, f, ensure_ascii=False)
                template_combo['values'] = ["بدون قالب"] + list(saved_templates.keys())
                template_var.set(t_name)
                messagebox.showinfo("نجاح", f"تم حفظ القالب: {t_name}")

        tk.Button(msg_frame, text="💾 حفظ كقالب جديد", command=save_template, bg="#FF9800", fg="white", font=('Segoe UI', 10)).grid(row=3, column=0, columnspan=2, pady=5)

        # Execution Frame
        exec_frame = tk.LabelFrame(right_frame, text="3️⃣ حالة الإرسال", font=('Segoe UI', 12, 'bold'), bg="#ffffff", padx=10, pady=10)
        exec_frame.pack(fill="both", expand=True, pady=5)

        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(exec_frame, variable=progress_var, maximum=100)
        progress_bar.pack(fill="x", pady=10)

        status_lbl = tk.Label(exec_frame, text="في انتظار بدء الإرسال...", bg="#ffffff", fg="blue", font=('Segoe UI', 10, 'bold'))
        status_lbl.pack(pady=2)

        time_lbl = tk.Label(exec_frame, text="الوقت المتبقي: ---", bg="#ffffff", fg="#d32f2f", font=('Segoe UI', 10, 'bold'))
        time_lbl.pack(pady=2)
        
        def send_action():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("تنبيه", "الرجاء تحديد طالب واحد على الأقل من القائمة!")
                return
                
            msg = msg_text.get("1.0", "end-1c").strip()
            if not msg:
                messagebox.showwarning("تنبيه", "الرسالة فارغة!")
                return
                
            contacts = []
            for item in selected:
                vals = tree.item(item, 'values')
                if vals[3]: # Has Phone
                    contacts.append({"name": vals[0], "phone": vals[3]})
                    
            if not contacts:
                messagebox.showerror("خطأ", "الطلاب المحددين ليس لديهم أرقام جوال مسجلة.")
                return

            btn_send.config(state="disabled")
            
            def p_callback(val):
                main_win.after(0, lambda: progress_var.set(val))
                
            def s_callback(msg):
                main_win.after(0, lambda: status_lbl.config(text=msg))
                
            def t_callback(msg):
                main_win.after(0, lambda: time_lbl.config(text=msg))

            def worker():
                try:
                    bot = WhatsAppSenderBot(headless=False, progress_callback=p_callback, status_callback=s_callback, time_callback=t_callback)
                    # batch size 40, wait 10s between msgs, 120s rest
                    bot.send_messages_batch(contacts, msg, batch_size=40, wait_between_messages=10, wait_between_batches=120)
                except Exception as e:
                    s_callback(f"عطل غیر متوقع: {e}")
                finally:
                    main_win.after(0, lambda: btn_send.config(state="normal"))

            threading.Thread(target=worker, daemon=True).start()

        btn_send = tk.Button(exec_frame, text="🚀 إرسال للمحددين (آلي بقوة Selenium)", command=send_action, bg="#25d366", fg="white", font=('Segoe UI', 13, 'bold'), cursor="hand2")
        btn_send.pack(fill="x", pady=15, ipady=5)

    # --- page_swap_request ---"""

start_marker = "    # --- send_whatsapp_to_parent ---"
end_marker = "    # --- page_swap_request ---"

if start_marker in content and end_marker in content:
    s_idx = content.find(start_marker)
    e_idx = content.find(end_marker)
    new_content = content[:s_idx] + new_gui_code + "\n" + content[e_idx:]
    with codecs.open('main_100_percent_v3.py', 'w', 'utf-8') as f:
        f.write(new_content)
    print("Patch fully created successfully!")
else:
    print("Failed to find markers.")
