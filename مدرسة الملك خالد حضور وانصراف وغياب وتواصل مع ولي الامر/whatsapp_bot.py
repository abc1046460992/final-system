import os
import time
import urllib.parse
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WhatsAppSenderBot:
    def __init__(self, headless=False, progress_callback=None, status_callback=None, time_callback=None):
        self.headless = headless
        self.progress_callback = progress_callback
        self.status_callback = status_callback
        self.time_callback = time_callback
        self.driver = None

    def _update_status(self, msg):
        if self.status_callback:
            self.status_callback(msg)

    def _update_progress(self, val):
        if self.progress_callback:
            self.progress_callback(val)

    def _update_time(self, expected_seconds_left):
        if self.time_callback:
            m, s = divmod(int(expected_seconds_left), 60)
            h, m = divmod(m, 60)
            time_str = ""
            if h > 0:
                time_str += f"{h} ساعة و "
            if m > 0:
                time_str += f"{m} دقيقة و "
            time_str += f"{s} ثانية"
            self.time_callback(f"الوقت المتبقي لإنهاء الإرسال: {time_str}")

    def init_driver(self):
        self._update_status("جاري تشغيل المتصفح (قد يستغرق بضع ثواني)...")
        options = Options()
        if self.headless:
            options.add_argument("--headless=new")

        # Session persistence
        base_path = os.path.dirname(os.path.abspath(__file__))
        user_data_dir = os.path.join(base_path, 'whatsapp_chrome_data')
        if not os.path.exists(user_data_dir):
            os.makedirs(user_data_dir)

        options.add_argument(f"user-data-dir={user_data_dir}")
        options.add_argument("--start-maximized")

        try:
            self.driver = webdriver.Chrome(options=options)
            return True
        except Exception as e:
            self._update_status(f"فشل في تشغيل المتصفح: {e}")
            return False

    def wait_for_login(self, timeout=60):
        self._update_status("جاري الاتصال بـ WhatsApp Web...")
        self.driver.get("https://web.whatsapp.com")
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, "//div[@id='pane-side']"))
            )
            self._update_status("تم الاتصال بوحدات WhatsApp بنجاح!")
            return True
        except:
            self._update_status("فشل قراءة WhatsApp! تأكد من ربط الجهاز بمسح الكود (QR).")
            return False

    def send_messages_batch(self, contacts, message_template, batch_size=40, wait_between_messages=10, wait_between_batches=120):
        """
        contacts: list of dicts [{'name': '...', 'phone': '966...'}, ...]
        """
        total = len(contacts)
        if total == 0:
            self._update_status("لا يوجد جهات اتصال للإرسال.")
            return

        if not self.init_driver():
            return

        if not self.wait_for_login():
            self.driver.quit()
            return

        sent_count = 0
        total_batches = (total + batch_size - 1) // batch_size

        for b_i in range(total_batches):
            start_idx = b_i * batch_size
            end_idx = min(start_idx + batch_size, total)
            batch = contacts[start_idx:end_idx]

            self._update_status(f"إرسال الدفعة {b_i+1} من {total_batches}...")

            for idx, contact in enumerate(batch):
                c_name = contact['name']
                c_phone = contact['phone']
                
                # Replace placeholders in message
                actual_message = message_template.replace("{اسمالطالب}", c_name).replace("{اسم_الطالب}", c_name)
                
                # Open Chat
                self._update_status(f"جاري الإرسال إلى {c_name} ({c_phone})...")
                
                try:
                    url = f"https://web.whatsapp.com/send?phone={c_phone}&text={urllib.parse.quote(actual_message)}"
                    self.driver.get(url)
                    
                    # Wait for input box to load
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.XPATH, "//footer//div[@contenteditable='true']"))
                    )
                    time.sleep(2) # extra second for complete load
                    
                    # Hit Enter
                    input_box = self.driver.find_element(By.XPATH, "//footer//div[@contenteditable='true']")
                    input_box.send_keys(Keys.ENTER)
                    
                    sent_count += 1
                    percent = (sent_count / total) * 100
                    self._update_progress(percent)
                    
                    # Calculations for time remaining
                    remaining_messages = total - sent_count
                    remaining_batches = remaining_messages // batch_size
                    expected_time = (remaining_messages * wait_between_messages) + (remaining_batches * wait_between_batches)
                    self._update_time(expected_time)

                    # Micro delay
                    time.sleep(wait_between_messages)
                    
                except Exception as e:
                    print(f"Failed to send to {c_phone}: {str(e)}")
                    # Proceed to next anyway
                    pass

            # Macro delay if not the last batch
            if b_i < total_batches - 1:
                self._update_status(f"استراحة محارب (حماية من الحظر) لمدة {wait_between_batches} ثانية...")
                # Update time countdown during rest
                for w in range(wait_between_batches, 0, -1):
                    time.sleep(1)
                    remaining_messages = total - sent_count
                    remaining_batches = remaining_messages // batch_size
                    # Approx time left = remaining rest time + future messages/batches time
                    expected_time = w + (remaining_messages * wait_between_messages) + (max(0, remaining_batches - 1) * wait_between_batches)
                    self._update_time(expected_time)
        
        self._update_progress(100)
        self._update_status("تم الانتهاء من الإرسال لجميع الأسماء بنجاح! 🎉")
        self._update_time(0)
        time.sleep(3)
        self.driver.quit()

