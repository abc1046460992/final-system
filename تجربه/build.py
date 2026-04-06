import os
import customtkinter
import PyInstaller.__main__

# الحصول على مسار مكتبة customtkinter لضمان ظهور الثيمات والخطوط في النسخة المجمعة
customtkinter_path = os.path.dirname(customtkinter.__file__)

print("بدأ تجميع التطبيق (قد يستغرق بعض الوقت)...")

PyInstaller.__main__.run([
    'app.py',
    '--name=WhatsAppBot_Pro',
    '--noconsole', # إخفاء نافذة الدوس السوداء
    '--onefile', # جعله ملفاً تنفيذياً واحداً
    '--icon=whatsapp.ico', # الأيقونة الخضراء المميزة
    f'--add-data={customtkinter_path};customtkinter/', # تضمين ملفات التصميم
    '--add-data=whatsapp.ico;.', # تضمين الأيقونة داخل البرنامج نفسه
    '--collect-all=selenium', # جمع كافة مكتبات سيلينيوم (بما فيها selenium-manager)
    '--clean', # مسح النسخ المؤقتة القديمة حتى يتم بناء التطبيق بآخر التحديثات
])

print("تم تجميع التطبيق بنجاح! ستجده في مجلد dist.")
