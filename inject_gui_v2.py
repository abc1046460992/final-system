import codecs

with codecs.open('main_100_percent_v3.py', 'r', 'utf-8') as f:
    content = f.read()

new_gui_code = """    # --- send_whatsapp_to_parent ---
    def send_whatsapp_to_parent(self, student_name=None):
        import json
        import threading
        from whatsapp_bot import WhatsAppSenderBot

        # Setup Templates & Senders File
        templates_file = data_path("whatsapp_templates.json")
        sender_file = data_path("whatsapp_senders.txt")
        
        default_templates = {
            "إشعار غياب": "المكرم ولي أمر الطالب {اسم_الطالب}، نود إشعاركم بغياب ابنكم عن المدرسة اليوم.",
            "إشعار تأخير": "المكرم ولي أمر الطالب {اسم_الطالب}، نود إشعاركم بتأخر ابنكم عن الطابور الصباحي اليوم."
        }
        if not os.path.exists(templates_file):
            with open(templates_file, "w", encoding="utf-8") as f:
                json.dump(default_templates, f, ensure_ascii=False)
        with open(templates_file, "r", encoding="utf-8") as f:
            saved_templates = json.load(f)

        saved_senders = []
        if os.path.exists(sender_file):
            with open(sender_file, "r", encoding="utf-8") as f:
                saved_senders = [line.strip() for line in f if line.strip()]

        main_win = tk.Toplevel(self)
        main_win.title("إرسال رسالة واتساب")
        main_win.geometry("1000x800")
        main_win.configure(bg="#f5f5f5") # light grey background match
        main_win.grab_set()

        # Header exactly like old
        header_lbl = tk.Label(main_win, text="📱 إرسال رسالة واتساب", font=('Segoe UI', 16, 'bold'), fg="#25d366", bg="#f5f5f5")
        header_lbl.pack(pady=10)
        
        # Instruction text as requested by user
        warn_text = "⚠️ تنبيه هام لمن يستخدم الأداة: يجب أولاً أن يكون المتصفح (Google Chrome) جاهزاً وتم مسح كود الـ QR الخاص بالواتساب ويب فيه ليتم الإرسال بنجاح."
        tk.Label(main_win, text=warn_text, font=('Segoe UI', 10, 'bold'), fg="#D32F2F", bg="#f5f5f5").pack(pady=(0,10))

        # Main Container to hold everything side by side or stacked (Stack in Old style)
        # 1. Sender Box
        sender_frame = tk.LabelFrame(main_win, text="1️⃣ رقم/اسم المرسل (المدرسة/المدير)", font=('Segoe UI', 11, 'bold'), padx=15, pady=10, bg="#f5f5f5")
        sender_frame.pack(fill="x", padx=20, pady=5)
        
        sender_var = tk.StringVar()
        if saved_senders:
            tk.Label(sender_frame, text="اختر من الأرقام المحفوظة:", font=('Segoe UI', 10), bg="#f5f5f5").pack(anchor="e", pady=2)
            sender_combo = ttk.Combobox(sender_frame, textvariable=sender_var, values=saved_senders, font=('Segoe UI', 11), state="readonly")
            sender_combo.pack(fill="x", pady=2)
            sender_combo.current(0)
            tk.Label(sender_frame, text="أو أضف مرسل جديد:", font=('Segoe UI', 10), bg="#f5f5f5").pack(anchor="e", pady=(5,0))

        new_sender_entry = tk.Entry(sender_frame, font=('Segoe UI', 11))
        new_sender_entry.pack(fill="x", pady=2)
        new_sender_entry.insert(0, "اسم أو رقم المرسل...")

        # Split rest into left/right for clarity, maintaining the old LabelFrame look
        middle_container = tk.Frame(main_win, bg="#f5f5f5")
        middle_container.pack(fill="both", expand=True, padx=20, pady=5)

        # 2. Receivers (Right side because Arabic)
        recipient_frame = tk.LabelFrame(middle_container, text="2️⃣ اختر المستقبل (الطلاب)", font=('Segoe UI', 11, 'bold'), padx=10, pady=10, bg="#f5f5f5")
        recipient_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))

        filter_frame = tk.Frame(recipient_frame, bg="#f5f5f5")
        filter_frame.pack(fill="x", pady=2)

        # Replicating the "Search" text entry look
        search_var = tk.StringVar()
        search_entry = tk.Entry(filter_frame, textvariable=search_var, font=('Segoe UI', 12))
        search_entry.pack(fill="x", pady=5)
        search_entry.insert(0, "اكتب اسم الطالب...")
        
        def on_s_in(e):
            if search_entry.get() == "اكتب اسم الطالب...": search_entry.delete(0, tk.END)
        def on_s_out(e):
            if not search_entry.get(): search_entry.insert(0, "اكتب اسم الطالب...")
        search_entry.bind("<FocusIn>", on_s_in)
        search_entry.bind("<FocusOut>", on_s_out)

        # Class/Section row
        c_s_frame = tk.Frame(filter_frame, bg="#f5f5f5")
        c_s_frame.pack(fill="x", pady=5)
        tk.Label(c_s_frame, text="الصف:", bg="#f5f5f5", font=('Segoe UI', 10)).pack(side="right")
        class_var = tk.StringVar(value="الكل")
        ttk.Combobox(c_s_frame, textvariable=class_var, values=["الكل", "أول متوسط", "ثاني متوسط", "ثالث متوسط"], state="readonly", width=12).pack(side="right", padx=5)
        
        tk.Label(c_s_frame, text="الشعبة:", bg="#f5f5f5", font=('Segoe UI', 10)).pack(side="right", padx=(10,0))
        section_var = tk.StringVar(value="الكل")
        ttk.Combobox(c_s_frame, textvariable=section_var, values=["الكل", "1", "2", "3", "4", "5", "6"], state="readonly", width=5).pack(side="right", padx=5)

        # List
        tree_frame = tk.Frame(recipient_frame, bg="#f5f5f5")
        tree_frame.pack(fill="both", expand=True, pady=5)
        tree_scroll = ttk.Scrollbar(tree_frame)
        tree_scroll.pack(side="left", fill="y")
        tree = ttk.Treeview(tree_frame, columns=("name", "phone"), show="headings", yscrollcommand=tree_scroll.set, selectmode="extended")
        tree.heading("name", text="اسم الطالب")
        tree.heading("phone", text="الرقم")
        tree.column("name", width=200, anchor="e")
        tree.column("phone", width=100, anchor="center")
        tree.pack(side="right", fill="both", expand=True)
        tree_scroll.config(command=tree.yview)

        def apply_filter(*args):
            for i in tree.get_children(): tree.delete(i)
            s_text = search_var.get().strip().lower()
            if s_text == "اكتب اسم الطالب...": s_text = ""
            c_filter = class_var.get()
            sec_filter = section_var.get()
            try:
                name_col, class_col, section_col = self.m._detect_student_cols()
                phone_col = None
                for col in self.m.df_students.columns:
                    if "جوال" in str(col).lower():
                        phone_col = col
                        break
                if not phone_col: return
                for _, row in self.m.df_students.iterrows():
                    name = tidy(row.get(name_col, ""))
                    stu_class = tidy(row.get(class_col, ""))
                    stu_sec = str(row.get(section_col, "")).split('.')[0]
                    phone = tidy(row.get(phone_col, ""))
                    if not name: continue
                    if phone:
                        phone = str(phone).replace(" ", "").replace("-", "")
                        if phone.startswith("0"): phone = "966" + phone[1:]
                        if not phone.startswith("966"): phone = "966" + phone
                    if s_text and s_text not in name.lower(): continue
                    if c_filter != "الكل" and c_filter not in stu_class: continue
                    if sec_filter != "الكل" and sec_filter != stu_sec: continue
                    tree.insert("", "end", values=(name, phone))
            except Exception as e:
                print(e)
                
        search_var.trace("w", lambda *a: apply_filter())
        class_var.trace("w", lambda *a: apply_filter())
        section_var.trace("w", lambda *a: apply_filter())
        
        btn_sel_frame = tk.Frame(recipient_frame, bg="#f5f5f5")
        btn_sel_frame.pack(fill="x", pady=2)
        tk.Button(btn_sel_frame, text="تحديد الكل", command=lambda: [tree.selection_add(i) for i in tree.get_children()], bg="#e0e0e0", fg="#333", relief="flat", padx=15).pack(side="right", padx=2)
        tk.Button(btn_sel_frame, text="إلغاء التحديد", command=lambda: tree.selection_remove(tree.selection()), bg="#e0e0e0", fg="#333", relief="flat", padx=15).pack(side="right", padx=2)
        
        apply_filter()

        # 3. Message (Left side)
        msg_frame = tk.LabelFrame(middle_container, text="3️⃣ الرسالة والاختصارات", font=('Segoe UI', 11, 'bold'), padx=10, pady=10, bg="#f5f5f5")
        msg_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))

        tk.Label(msg_frame, text="اختر قالب (اختصار):", bg="#f5f5f5", font=('Segoe UI', 10)).pack(anchor="e")
        template_var = tk.StringVar()
        template_combo = ttk.Combobox(msg_frame, textvariable=template_var, values=["بدون قالب"] + list(saved_templates.keys()), state="readonly")
        template_combo.pack(fill="x", pady=5)
        template_combo.current(0)

        msg_text = tk.Text(msg_frame, font=('Segoe UI', 11), wrap="word", height=8)
        msg_text.pack(fill="both", expand=True, pady=5)
        msg_text.insert("1.0", "السلام عليكم ورحمة الله وبركاته،\\n")

        tk.Label(msg_frame, text="* استخدم المتغير {اسم_الطالب} في رسالتك", bg="#f5f5f5", fg="#666", font=('Segoe UI', 9)).pack(anchor="e")

        def on_template_select(e):
            sel = template_var.get()
            if sel in saved_templates:
                msg_text.delete("1.0", tk.END)
                msg_text.insert("1.0", saved_templates[sel])
        template_combo.bind("<<ComboboxSelected>>", on_template_select)

        def save_template():
            t_name = tk.simpledialog.askstring("حفظ الاختصار", "اسم الاختصار السريع للرسالة:", parent=main_win)
            if t_name:
                saved_templates[t_name] = msg_text.get("1.0", "end-1c").strip()
                with open(templates_file, "w", encoding="utf-8") as f: json.dump(saved_templates, f, ensure_ascii=False)
                template_combo['values'] = ["بدون قالب"] + list(saved_templates.keys())
                template_var.set(t_name)
                messagebox.showinfo("نجاح", f"تم حفظ قالب: {t_name}")
        tk.Button(msg_frame, text="💾 حفظ الرسالة كاختصار", command=save_template, bg="#e0e0e0", fg="#333", relief="flat", padx=10).pack(pady=5)

        # 4. Status and Send Bottom Bar
        bottom_frame = tk.LabelFrame(main_win, text="4️⃣ حالة الإرسال", bg="#f5f5f5", font=('Segoe UI', 11, 'bold'), padx=10, pady=10)
        bottom_frame.pack(fill="x", padx=20, pady=5)

        info_frame = tk.Frame(bottom_frame, bg="#f5f5f5")
        info_frame.pack(fill="x", pady=5)
        
        status_lbl = tk.Label(info_frame, text="حالة الخوادم جاهزة...", bg="#f5f5f5", fg="#128c7e", font=('Segoe UI', 10, 'bold'))
        status_lbl.pack(side="right", padx=10)
        
        time_lbl = tk.Label(info_frame, text="الوقت المتبقي: ---", bg="#f5f5f5", fg="#d32f2f", font=('Segoe UI', 10, 'bold'))
        time_lbl.pack(side="left", padx=10)

        progress_var = tk.DoubleVar()
        progress_bar = ttk.Progressbar(bottom_frame, variable=progress_var, maximum=100)
        progress_bar.pack(fill="x", pady=5)

        btn_frame = tk.Frame(main_win, bg="#f5f5f5")
        btn_frame.pack(pady=10)

        def send_action():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("تنبيه", "حدد طالباً واحداً على الأقل!")
                return
            msg = msg_text.get("1.0", "end-1c").strip()
            if not msg:
                messagebox.showwarning("تنبيه", "الرسالة فارغة!")
                return
            
            # Save new sender
            s_phone = new_sender_entry.get().strip()
            if s_phone and s_phone != "اسم أو رقم المرسل..." and s_phone not in saved_senders:
                with open(sender_file, "a", encoding="utf-8") as f:
                    f.write(s_phone + "\\n")

            contacts = []
            for item in selected:
                vals = tree.item(item, 'values')
                if vals[1]: contacts.append({"name": vals[0], "phone": vals[1]})
            if not contacts:
                messagebox.showerror("خطأ", "هؤلاء الطلاب ليس لديهم هواتف")
                return

            btn_send.config(state="disabled", bg="#999")
            
            def p_cb(val): main_win.after(0, lambda: progress_var.set(val))
            def s_cb(text): main_win.after(0, lambda: status_lbl.config(text=text))
            def t_cb(text): main_win.after(0, lambda: time_lbl.config(text=text))

            def worker():
                try:
                    bot = WhatsAppSenderBot(headless=False, progress_callback=p_cb, status_callback=s_cb, time_callback=t_cb)
                    bot.send_messages_batch(contacts, msg, batch_size=40, wait_between_messages=10, wait_between_batches=120)
                except Exception as e:
                    s_cb(f"عطل: {e}")
                finally:
                    main_win.after(0, lambda: btn_send.config(state="normal", bg="#25d366"))
            threading.Thread(target=worker, daemon=True).start()

        btn_send = tk.Button(btn_frame, text="📤 إرسال عبر واتساب (متعدد)", command=send_action, bg="#25d366", fg="white", font=('Segoe UI', 12, 'bold'), padx=30, pady=10, relief="flat", cursor="hand2")
        btn_send.pack(side="right", padx=10)
        tk.Button(btn_frame, text="إلغاء", command=main_win.destroy, bg="#999", fg="white", font=('Segoe UI', 11), padx=30, pady=10, relief="flat", cursor="hand2").pack(side="right", padx=10)

    # --- page_swap_request ---"""

start_marker = "    # --- send_whatsapp_to_parent ---"
end_marker = "    # --- page_swap_request ---"

if start_marker in content and end_marker in content:
    s_idx = content.find(start_marker)
    e_idx = content.find(end_marker)
    new_content = content[:s_idx] + new_gui_code + "\n" + content[e_idx:]
    with codecs.open('main_100_percent_v3.py', 'w', 'utf-8') as f:
        f.write(new_content)
    print("V2 Patch successfully injected!")
else:
    print("Failed to find markers.")
