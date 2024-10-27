from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from utils.macros import EMAIL_PATTERN, PASSWORD_PATTERN
from concurrent.futures import ThreadPoolExecutor
from kivy.clock import mainthread, Clock
from models.student_model import Student
from models.admin_model import Admin
from helpers.email_helper import send_mail, get_verification_code_content
import os, random, string, re
import hashlib

Builder.load_file('views/reset_password_view.kv')

class ResetPasswordView(Screen):
    def on_enter(self):
        self.ed_squared_app = App.get_running_app()
        self.verification_code = None
        self.executor = ThreadPoolExecutor(max_workers=1)

    def validate_fields(self, email, password, confirm_password):
        if not email or not password:
            self.ids.reset_password_message.text = 'All fields are required.'
            return False

        if re.match(EMAIL_PATTERN, email) is None:
            self.ids.reset_password_message.text = 'Not a valid email.'
            return False

        if re.match(PASSWORD_PATTERN, password) is None:
            self.ids.reset_password_message.text = '''
            Not a valid Password. Minimum 8 characters long.
            Must have atleast 1 alphabet, 1 number,
            1 special character.
            '''
            return False

        if password != confirm_password:
            self.ids.reset_password_message.text = 'Passwords do not match.'
            return False

        self.ids.reset_password_message.text = ""
        return True

    def generate_(self):
        spinner = self.ids.spinner
        spinner.active = True
        spinner.size = (dp(40), dp(40))

        future = self.executor.submit(self.generate_verification_code)
        future.add_done_callback(lambda future: Clock.schedule_once(lambda dt: self.data_loaded(future.result()), 0))

    @mainthread
    def data_loaded(self, data, *args):
        spinner = self.ids.spinner
        spinner.active = False
        spinner.size = (dp(0), dp(0))
        self.ids.reset_password_message.text = data

    def generate_verification_code(self):

        self.verification_code = ''.join(random.choices(string.digits, k=6))

        mail_dict = get_verification_code_content(self.ids.email_input.text, self.verification_code)
        success = send_mail(mail_dict["SENDER_MAIL"], mail_dict["RECEIVER_MAIL"], mail_dict["EMAIL_SUBJECT"], mail_dict["EMAIL_BODY"])

        if success:
            return "Check your mail/spam for code."

        return "Please try again."

    def hash_password(self, password):
        salt = os.urandom(16)

        hash_obj = hashlib.sha256(salt + password.encode('utf-8'))
        hashed_password = hash_obj.hexdigest()
        salt_and_hashed_password = salt.hex() + hashed_password

        return salt_and_hashed_password

    def reset_password(self, user_email, new_password, confirm_password, verification_code):
        if self.validate_fields(user_email, new_password, confirm_password):
            if verification_code == self.verification_code:
                user_obj = None
                if self.ids.admin_checkbox.active:
                    user_obj = Admin()
                    user_details = user_obj.get_admin_details(user_email)
                else:
                    user_obj = Student()
                    user_details = user_obj.get_student_details(user_email)
                if user_details:
                    hashed_password = self.hash_password(new_password)
                    if user_obj.update_password(user_details["ID"], hashed_password):
                        self.ids.reset_password_message.text = "Password Updated."
                    else:
                        self.ids.reset_password_message.text = "Failed process. Try Again."
                else:
                    self.ids.reset_password_message.text = "No Such user exists."
            else:
                self.ids.reset_password_message.text = "Invalid Verification Code"
        else:
            self.ids.reset_password_message.text = "Check fields again."
