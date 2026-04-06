import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WhatsAppDriver:
    def __init__(self, headless=False):
        self.options = Options()
        if headless:
            self.options.add_argument("--headless=new")

        base_path = os.path.dirname(os.path.abspath(__file__))
        user_data_dir = os.path.join(base_path, 'chrome_data')

        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)

        self.options.add_argument(f"user-data-dir={user_data_dir}")
        self.options.add_argument("--start-maximized")

        try:
            self.driver = webdriver.Chrome(options=self.options)
        except Exception as e:
            print(f"❌ خطأ أثناء تشغيل المتصفح: {e}")
            raise

    # ===============================
    def load_session(self):
        print("📱 فتح واتساب")
        self.driver.get("https://web.whatsapp.com")
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='pane-side']"))
            )
            print("✅ تم تسجيل الدخول")
            return True
        except:
            print("❌ فشل تسجيل الدخول")
            return False

    # ===============================
    def open_chat(self, phone):
        phone = phone.replace("+", "")
        print(f"📤 فتح المحادثة: {phone}")
        self.driver.get(f"https://web.whatsapp.com/send?phone={phone}&app_absent=0")
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((
                    By.XPATH, "//footer//div[@contenteditable='true']"
                ))
            )
            print("✅ تم تحميل المحادثة")
            return True
        except:
            print("❌ لم يتم تحميل المحادثة")
            return False

    # ===============================
    def debug_footer(self):
        """اطبع كل العناصر في footer لمعرفة الـ selector الصحيح"""
        print("\n" + "="*60)
        print("🔍 DEBUG: فحص عناصر الـ footer")
        print("="*60)

        spans = self.driver.find_elements(By.XPATH, "//footer//span[@data-icon]")
        print(f"\n📌 spans بـ data-icon ({len(spans)}):")
        for el in spans:
            try:
                print(f"   data-icon='{el.get_attribute('data-icon')}'")
            except:
                pass

        btns = self.driver.find_elements(By.XPATH, "//footer//div[@role='button']")
        print(f"\n📌 buttons في footer ({len(btns)}):")
        for el in btns:
            try:
                aria  = el.get_attribute("aria-label") or ""
                title = el.get_attribute("title") or ""
                tid   = el.get_attribute("data-testid") or ""
                print(f"   aria='{aria}'  title='{title}'  testid='{tid}'")
            except:
                pass

        titled = self.driver.find_elements(By.XPATH, "//footer//*[@title]")
        print(f"\n📌 عناصر بـ title ({len(titled)}):")
        for el in titled:
            try:
                print(f"   <{el.tag_name}> title='{el.get_attribute('title')}'")
            except:
                pass

        print("="*60 + "\n")

    # ===============================
    def _click_attach_btn(self):
        selectors = [
            "//footer//span[@data-icon='plus']",
            "//footer//*[@data-icon='plus']",
            "//footer//span[@data-icon='clip']",
            "//footer//*[@data-icon='clip']",
            "//footer//span[@data-icon='attach-menu-plus']",
            "//footer//div[@aria-label='إرفاق']",
            "//footer//div[@aria-label='Attach']",
            "//footer//*[@title='إرفاق']",
            "//footer//*[@title='Attach']",
            "//footer//*[@data-testid='attach-btn']",
        ]
        for sel in selectors:
            try:
                btn = WebDriverWait(self.driver, 3).until(
                    EC.element_to_be_clickable((By.XPATH, sel))
                )
                self.driver.execute_script("arguments[0].click();", btn)
                print(f"✅ ضغط زر الإرفاق: {sel}")
                return True
            except:
                continue
        print("❌ فشل إيجاد زر الإرفاق")
        return False

    # ===============================
    def send_message(self, phone, text="", file_path=None):
        try:
            if not self.open_chat(phone):
                return False

            time.sleep(2)

            # ===== نص فقط =====
            if text and not file_path:
                input_box = self.driver.find_element(
                    By.XPATH, "//footer//div[@contenteditable='true']"
                )
                input_box.send_keys(text)
                input_box.send_keys(Keys.ENTER)
                print("✅ تم إرسال النص")
                return True

            # ===== إرسال كمستند =====
            if file_path:
                file_path = os.path.abspath(file_path)

                if not os.path.exists(file_path):
                    print(f"❌ الملف غير موجود: {file_path}")
                    return False

                print(f"📎 إرسال: {os.path.basename(file_path)}")

                # 1. زر الإرفاق
                if not self._click_attach_btn():
                    self.debug_footer()   # اطبع DOM للتشخيص
                    return False

                time.sleep(1.5)

                # 2. اختر "مستند"
                print("📄 اختيار مستند...")
                doc_clicked = False
                for sel in [
                    "//span[normalize-space()='مستند']",
                    "//span[normalize-space()='Document']",
                    "//li[.//span[contains(text(),'ستند')]]",
                    "//li[.//span[contains(text(),'ocument')]]",
                ]:
                    try:
                        btn = WebDriverWait(self.driver, 4).until(
                            EC.element_to_be_clickable((By.XPATH, sel))
                        )
                        self.driver.execute_script("arguments[0].click();", btn)
                        print("✅ تم اختيار مستند")
                        doc_clicked = True
                        time.sleep(1)
                        break
                    except:
                        continue

                if not doc_clicked:
                    print("⚠️ خيار مستند غير موجود — المتابعة")

                # 3. أرسل الملف للـ input
                print("📂 رفع الملف...")
                file_inputs = self.driver.find_elements(
                    By.XPATH, "//input[@type='file']"
                )

                if not file_inputs:
                    print("❌ لا توجد inputs")
                    return False

                for i, inp in enumerate(file_inputs):
                    try:
                        print(f"   input[{i}] accept='{inp.get_attribute('accept')}'")
                    except:
                        pass

                file_inputs[0].send_keys(file_path)

                # 4. انتظر المعاينة
                print("⏳ انتظار المعاينة...")
                time.sleep(5)

                # 5. كابشن
                if text:
                    try:
                        caption = self.driver.find_element(
                            By.XPATH, "//div[@contenteditable='true']"
                        )
                        caption.send_keys(text)
                    except:
                        pass

                # 6. إرسال
                print("🚀 إرسال...")
                send_btn = WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        "//div[@aria-label='إرسال'] | //span[@data-icon='wds-ic-send-filled']"
                    ))
                )
                self.driver.execute_script("""
                    arguments[0].scrollIntoView(true);
                    arguments[0].click();
                """, send_btn)

                print("🟢 تم الإرسال!")
                print("⏳ انتظار 15 ثانية...")
                time.sleep(15)
                return True

            return False

        except Exception as e:
            import traceback
            print(f"❌ خطأ: {e}")
            print(traceback.format_exc())
            return False

    def close(self):
        self.driver.quit()