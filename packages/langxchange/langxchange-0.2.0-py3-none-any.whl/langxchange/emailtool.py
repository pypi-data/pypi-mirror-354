# langxchange/email_tool.py

import time
import random
import string
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from email_validator import validate_email, EmailNotValidError
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from typing import List, Dict, Any  # <-- Added this line


class EmailTool:
    def __init__(self, captcha_api_key=None, headless=False, proxy=None):
        """
        Initialize the EmailTool with optional CAPTCHA solving service API key.

        Args:
            captcha_api_key (str): API key for CAPTCHA solving service (e.g., 2Captcha)
            headless (bool): Run browser in headless mode
            proxy (str): Proxy server in format 'ip:port' or 'user:pass@ip:port'
        """
        self.captcha_api_key = captcha_api_key
        self.driver = None
        self.current_email = None
        self.current_password = None
        self.headless = headless
        self.proxy = proxy
        self.setup_browser()

    def setup_browser(self):
        """Initialize the Selenium WebDriver with configured options."""
        options = Options()
        # options = webdriver.Options()
        if self.headless:
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')

        if self.proxy:
            options.add_argument(f'--proxy-server={self.proxy}')

        # options.add_argument('--no-sandbox')
        # options.add_argument('--disable-dev-shm-usage')
        # options.add_argument('--disable-notifications')
        options.add_argument('--start-maximized')

        # options.add_argument('--disable-web-security')
        # # options.add_argument('--user-data-dir')
        # options.add_argument('--allow-running-insecure-content')
        # options.add_argument('--start-maximized')

        # Disable automation flags
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option('useAutomationExtension', False)
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.media_stream_mic": 1,
            "profile.default_content_setting_values.media_stream_camera": 1,
            "profile.default_content_setting_values.geolocation": 0,
            "profile.default_content_setting_values.notifications": 1
        })

        self.driver = webdriver.Chrome(options=options)

        # Modify navigator.webdriver flag to prevent detection
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    def generate_random_credentials(self):
        """Generate random email username and password."""
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
        password = ''.join(random.choices(string.ascii_letters + string.digits + '!@#$%^&*', k=16))
        return username, password

    def solve_captcha(self, site_key=None, url=None, captcha_type='image'):
        """
        Solve CAPTCHA using external service or built-in methods.

        Args:
            site_key (str): Site key for reCAPTCHA
            url (str): URL where CAPTCHA is located
            captcha_type (str): Type of CAPTCHA ('image' or 'recaptcha')

        Returns:
            str: CAPTCHA solution
        """
        if not self.captcha_api_key:
            raise ValueError("CAPTCHA API key is required for solving CAPTCHAs")

        if captcha_type == 'recaptcha' and site_key and url:
            # Use 2Captcha or similar service for reCAPTCHA
            import requests
            params = {
                'key': self.captcha_api_key,
                'method': 'userrecaptcha',
                'googlekey': site_key,
                'pageurl': url,
                'json': 1
            }

            # Submit CAPTCHA to solving service
            response = requests.post('http://2captcha.com/in.php', data=params)
            request_id = response.json().get('request')

            if not request_id:
                raise Exception("Failed to submit CAPTCHA to solving service")

            # Wait for solution
            for _ in range(30):  # 30 attempts with 5-second delays
                time.sleep(5)
                result = requests.get(
                    f'http://2captcha.com/res.php?key={self.captcha_api_key}'
                    f'&action=get&id={request_id}&json=1'
                ).json()

                if result.get('status') == 1:
                    return result.get('request')

            raise TimeoutError("CAPTCHA solving timed out")

        elif captcha_type == 'image':
            # For image CAPTCHAs, you would typically use OCR or similar service
            # This is a placeholder implementation
            captcha_element = self.driver.find_element(By.XPATH, "//img[contains(@alt, 'CAPTCHA')]")
            captcha_solution = "placeholder"  # In practice, you'd send this to a solving service
            return captcha_solution

        else:
            raise ValueError("Unsupported CAPTCHA type")

    def create_gmail_account(self, first_name=None, last_name=None):
        """
        Create a new Gmail account using browser automation.

        Args:
            first_name (str): First name for the account
            last_name (str): Last name for the account

        Returns:
            tuple: (email, password) of the created account
        """
        if not first_name or not last_name:
            first_name = ''.join(random.choices(string.ascii_lowercase, k=5))
            last_name = ''.join(random.choices(string.ascii_lowercase, k=7))

        username, password = self.generate_random_credentials()
        self.current_email = f"{username}@gmail.com"
        self.current_password = password

        # Navigate to Gmail account creation page
        self.driver.get('https://accounts.google.com/signup')

        try:
            # Fill in personal info
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'firstName'))
            )
            self.driver.find_element(By.NAME, 'firstName').send_keys(first_name)
            self.driver.find_element(By.NAME, 'lastName').send_keys(last_name)
            self.driver.find_element(By.XPATH, "//button[@type='button']").click()

            # Fill in birthday and gender
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'day'))
            )
            self.driver.find_element(By.NAME, 'day').send_keys(str(random.randint(1, 28)))
            self.driver.find_element(By.NAME, 'year').send_keys(str(random.randint(1980, 2000)))
            self.driver.find_element(By.NAME, 'gender').click()
            gender_options = self.driver.find_elements(By.XPATH, "//div[@role='option']")
            random.choice(gender_options).click()
            self.driver.find_element(By.XPATH, "//button[@type='button']").click()

            # Choose email
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'selectioni0'))
            )
            self.driver.find_element(By.ID, 'selectioni0').click()
            self.driver.find_element(By.NAME, 'Username').clear()
            self.driver.find_element(By.NAME, 'Username').send_keys(username)
            self.driver.find_element(By.XPATH, "//button[@type='button']").click()

            # Set password
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, 'Passwd'))
            )
            self.driver.find_element(By.NAME, 'Passwd').send_keys(password)
            self.driver.find_element(By.NAME, 'PasswdAgain').send_keys(password)
            self.driver.find_element(By.XPATH, "//button[@type='button']").click()

            # Handle phone verification (skipping for this example)
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Skip')]"))
            )
            skip_button = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'Skip')]")
            if skip_button:
                skip_button[0].click()

            # Handle CAPTCHA if present
            try:
                captcha_frame = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "//iframe[contains(@src, 'recaptcha')]"))
                )
                if captcha_frame:
                    site_key = captcha_frame.get_attribute('data-sitekey')
                    if site_key and self.captcha_api_key:
                        solution = self.solve_captcha(site_key=site_key, url=self.driver.current_url)
                        self.driver.execute_script(
                            f"document.getElementById('g-recaptcha-response').innerHTML='{solution}';"
                        )
                        time.sleep(2)
                        self.driver.find_element(By.XPATH, "//button[@type='button']").click()
            except TimeoutException:
                pass

            # Accept terms
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//button[@type='button']"))
            )
            self.driver.find_element(By.XPATH, "//button[@type='button']").click()

            # Wait for account creation to complete
            WebDriverWait(self.driver, 30).until(
                lambda d: 'myaccount.google.com' in d.current_url
            )

            return self.current_email, self.current_password

        except Exception as e:
            self.driver.save_screenshot('gmail_creation_error.png')
            raise Exception(f"Failed to create Gmail account: {str(e)}")

    def login_to_gmail(self, email: str, password: str) -> bool:
        """
        Log in to a Gmail account using browser automation.

        Args:
            email (str): Gmail address
            password (str): Account password

        Returns:
            bool: True if login successful
        """
        self.current_email = email
        self.current_password = password

        try:
            # self.driver.get("https://accounts.google.com/login")
            # driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver.get(r'https://accounts.google.com/v3/signin/challenge/pwd?TL=ALgCv6ztxxoQjiieE9puALOqxj0tH9Q6bVscapLsztCwZ3I4gZnbo_dXrJtgAyDr&cid=1&continue=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&dsh=S-1122570837%3A1748944217800299&emr=1&flowEntry=ServiceLogin&flowName=GlifWebSignIn&followup=https%3A%2F%2Fmail.google.com%2Fmail%2Fu%2F0%2F&ifkv=AdBytiMzrMjIV0esTmnh2qt8Ecb4FvyhDuKArvgoYxMm66xP-mGakMaN3ZIK2ClJIOirPP7cE_oM3w&osid=1&service=mail')
            # self.driver.get(r'https://accounts.google.com/signin/v2/identifier?continue='+\
            # 'https%3A%2F%2Fmail.google.com%2Fmail%2F&amp;service=mail&amp;sacu=1&amp;rip=1'+\
            # '&amp;flowName=GlifWebSignIn&amp;flowEntry = ServiceLogin')
            self.driver.implicitly_wait(15)
            # Enter email
            # WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.NAME, "identifier"))
            # )
            # self.driver.find_element(By.NAME, "identifier").send_keys(email)
            # self.driver.find_element(By.ID, "identifierNext").click()

            # Enter password
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
            self.driver.find_element(By.NAME, "password").send_keys(password)
            self.driver.find_element(By.ID, "passwordNext").click()

            # Verify login success
            WebDriverWait(self.driver, 30).until(
                lambda d: ("myaccount.google.com" in d.current_url)
                          or ("mail.google.com" in d.current_url)
            )

            return True

        except Exception as e:
            self.driver.save_screenshot("gmail_login_error.png")
            raise Exception(f"Failed to login to Gmail account: {str(e)}")
    
    def login_to_gmailA(self, email: str, password: str) -> bool:
        """
        Log in to a Gmail account using browser automation.

        Args:
            email (str): Gmail address
            password (str): Account password

        Returns:
            bool: True if login successful
        """
        self.current_email = email
        self.current_password = password

        try:
            self.driver.get('https://accounts.google.com/ServiceLogin?hl=en&passive=true&continue=https://www.google.com/&ec=GAZAAQ')

            # input Gmail
            self.driver.find_element(By.ID, "identifierId").send_keys(self.current_email)
            self.driver.find_element(By.ID, "identifierNext").click()
            self.driver.implicitly_wait(10)

            # input Password
            self.driver.find_element(By.XPATH,'//*[@id="password"]/div[1]/div/div[1]/input').send_keys(self.current_password)
            self.driver.implicitly_wait(10)
            self.driver.find_element(By.ID, "passwordNext").click()
            self.driver.implicitly_wait(10)

            # go to google home page
            self.driver.get('https://google.com/')
            self.driver.implicitly_wait(100)

           # Verify login success
            WebDriverWait(self.driver, 30).until(
                lambda d: ("myaccount.google.com" in d.current_url)
                          or ("mail.google.com" in d.current_url)
            )

            return True

        except Exception as e:
            self.driver.save_screenshot("gmail_login_error.png")
            raise Exception(f"Failed to login to Gmail account: {str(e)}")

    def read_emails(self, limit: int = 5, unread_only: bool = False) -> List[Dict[str, Any]]:
        """
        Read emails from the current Gmail account using IMAP.

        Args:
            limit (int): Maximum number of emails to retrieve
            unread_only (bool): Only fetch unread emails

        Returns:
            list: List of email messages (dict with subject, from, body, etc.)
        """
        if not self.current_email or not self.current_password:
            raise ValueError("No email account is currently logged in")

        try:
            # Connect to Gmail IMAP server
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.current_email, self.current_password)
            mail.select("inbox")

            # Search for emails
            search_criteria = "(UNSEEN)" if unread_only else "ALL"
            status, messages = mail.search(None, search_criteria)
            if status != "OK":
                raise Exception("Failed to search emails")

            email_ids = messages[0].split()[:limit]
            emails: List[Dict[str, Any]] = []

            for email_id in email_ids:
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                if status != "OK":
                    continue

                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)

                email_info: Dict[str, Any] = {
                    "subject": msg["subject"],
                    "from": msg["from"],
                    "date": msg["date"],
                    "body": self._extract_email_body(msg)
                }
                emails.append(email_info)

            mail.close()
            mail.logout()
            return emails

        except Exception as e:
            raise Exception(f"Failed to read emails: {str(e)}")

    def _extract_email_body(self, msg: email.message.Message) -> str:
        """Extract the body text from an email message."""
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    return part.get_payload(decode=True).decode(errors="ignore")
        else:
            return msg.get_payload(decode=True).decode(errors="ignore")
        return ""

    def verify_email(self, verification_link: str) -> bool:
        """
        Verify an email by visiting the verification link.

        Args:
            verification_link (str): URL of the verification link

        Returns:
            bool: True if verification successful
        """
        try:
            self.driver.get(verification_link)
            WebDriverWait(self.driver, 30).until(
                lambda d: ("verified" in d.current_url.lower()) or ("success" in d.current_url.lower())
            )
            return True
        except Exception as e:
            self.driver.save_screenshot("email_verification_error.png")
            raise Exception(f"Failed to verify email: {str(e)}")

    def send_email(self, to_email: str, subject: str, body: str, is_html: bool = False) -> bool:
        """
        Send an email from the current Gmail account.

        Args:
            to_email (str): Recipient email address
            subject (str): Email subject
            body (str): Email body content
            is_html (bool): Whether the body is HTML content

        Returns:
            bool: True if email sent successfully
        """
        if not self.current_email or not self.current_password:
            raise ValueError("No email account is currently logged in")

        try:
            # Validate recipient email
            try:
                validate_email(to_email)
            except EmailNotValidError as e:
                raise ValueError(f"Invalid recipient email: {str(e)}")

            # Create message
            msg = MIMEMultipart()
            msg["From"] = self.current_email
            msg["To"] = to_email
            msg["Subject"] = subject

            # Attach body
            if is_html:
                msg.attach(MIMEText(body, "html"))
            else:
                msg.attach(MIMEText(body, "plain"))

            # Send email via SMTP
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(self.current_email, self.current_password)
                smtp.send_message(msg)

            return True

        except Exception as e:
            raise Exception(f"Failed to send email: {str(e)}")

    def turnOffMicCam():
        # turn off Microphone
        time.sleep(2)
        self.driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[1]/div/div/div').click()
        self.driver.implicitly_wait(3000)

        # turn off camera
        time.sleep(1)
        self.driver.find_element(By.XPATH,'//*[@id="yDmH0d"]/c-wiz/div/div/div[8]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[2]/div/div').click()
        self.driver.implicitly_wait(3000)


    def joinNow():
        # Join meet
        print(1)
        time.sleep(5)
        self.driver.implicitly_wait(2000)
        self.driver.find_element(By.CSS_SELECTOR,
        'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
        print(1)


    def AskToJoin():
        # Ask to Join meet
        time.sleep(5)
        driver.implicitly_wait(2000)
        driver.find_element(By.CSS_SELECTOR,
        'div.uArJ5e.UQuaGc.Y5sE8d.uyXBBb.xKiqt').click()
        # Ask to join and join now buttons have same xpaths
    def close(self):
        """Clean up and close the browser."""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
