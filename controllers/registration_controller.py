from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.metrics import dp
from concurrent.futures import ThreadPoolExecutor
from kivy.clock import mainthread, Clock
from models.student_model import Student
from models.admin_model import Admin
from utils.macros import EMAIL_PATTERN, PASSWORD_PATTERN
from helpers.email_helper import send_mail, get_tutor_code_mail_content, get_student_registration_update_mail
import re
import hashlib
import os
import random
import string


Builder.load_file('views/registration_view.kv')

class RegistrationView(Screen):
    def on_enter(self):
        self.admin_code = None
        self.executor = ThreadPoolExecutor(max_workers=1)

    def register(self, first_name, last_name, email, password, confirm_password):
        first_name, last_name, email, password = self.sanitize_fields(first_name, last_name, email, password)
        if self.validate_fields(first_name, last_name, email, password, confirm_password):
            hashed_password = self.hash_password(password)
            user = None
            response = None
            if self.ids.admin_checkbox.active:
                user = "Admin"
                admin_obj = Admin()
                #
                if self.ids.six_digit_code.text == self.admin_code:
                    response = admin_obj.register_admin(first_name, last_name, email, hashed_password, self.ids.six_digit_code.text)
                else:
                    self.ids.registration_message.text = 'Invalid Tutor Code.'
                #
            else:
                user = "Student"
                student_obj = Student()
                #
                if self.ids.six_digit_code.text:
                    admin_code = self.ids.six_digit_code.text
                    response = student_obj.register_student(email, first_name, last_name, hashed_password, admin_code)
                else:
                    self.ids.registration_message.text = 'Tutor Code Required.'
                #

            if response:
                print(f"{user} {email} Registered.")
                if user == "Student":
                    mail_dict = get_student_registration_update_mail(response[1], self.ids.first_name_input.text, self.ids.last_name_input.text, self.ids.email_input.text)
                    send_mail(mail_dict["SENDER_MAIL"], mail_dict["RECEIVER_MAIL"], mail_dict["EMAIL_SUBJECT"], mail_dict["EMAIL_BODY"])
                self.ids.first_name_input.text = ''
                self.ids.last_name_input.text = ''
                self.ids.email_input.text = ''
                self.ids.password_input.text = ''
                self.ids.confirm_password_input.text = ''
                self.ids.six_digit_code.text = ''
                self.manager.change_screen('login_view')
            else:
                print(f"{user} {email} Not Registered.")
                self.ids.registration_message.text = f"{user} {email} Not Registered."

    def validate_fields(self, first_name, last_name, email, password, confirm_password):
        if not first_name or not last_name or not email or not password:
            self.ids.registration_message.text = 'All fields are required.'
            return False

        if re.match(EMAIL_PATTERN, email) is None:
            self.ids.registration_message.text = 'Not a valid email.'
            return False

        if re.match(PASSWORD_PATTERN, password) is None:
            self.ids.registration_message.text = '''
            Not a valid Password. Minimum 8 characters long.
            Must have atleast 1 alphabet, 1 number,
            1 special character.
            '''
            return False

        if password != confirm_password:
            self.ids.registration_message.text = 'Passwords do not match.'
            return False

        self.ids.registration_message.text = ""
        return True

    def sanitize_fields(self, first_name, last_name, email, password):
        first_name = first_name.strip().upper()
        last_name = last_name.strip().upper()
        email = email.strip().upper()
        password = password.strip()
        return first_name, last_name, email, password

    def hash_password(self, password):
        # Generate a random salt
        salt = os.urandom(16)

        # Hash the password with the generated salt using SHA-256
        hash_obj = hashlib.sha256(salt + password.encode('utf-8'))
        hashed_password = hash_obj.hexdigest()

        # Combine the salt and the hashed password
        salt_and_hashed_password = salt.hex() + hashed_password

        # Return the combined salt and hashed password as a string
        return salt_and_hashed_password

    def generate_(self):
        spinner = self.ids.spinner
        spinner.active = True
        spinner.size = (dp(40), dp(40))

        future = self.executor.submit(self.generate_admin_code)
        future.add_done_callback(lambda future: Clock.schedule_once(lambda dt: self.data_loaded(future.result()), 0))

    @mainthread
    def data_loaded(self, data, *args):
        spinner = self.ids.spinner
        spinner.active = False
        spinner.size = (dp(0), dp(0))
        self.ids.registration_message.text = data

    def generate_admin_code(self):
        if self.ids.admin_checkbox.active:
            admin_mail = self.ids.email_input.text
            if len(admin_mail) < 3:
                self.ids.registration_message.text = 'Invalid Email.'
                return

            first_three = admin_mail[:3].upper()

            last_three = ''.join(random.choices(string.digits, k=3))

            self.admin_code = first_three + last_three

            mail_dict = get_tutor_code_mail_content(self.ids.email_input.text, self.admin_code)
            success = send_mail(mail_dict["SENDER_MAIL"], mail_dict["RECEIVER_MAIL"], mail_dict["EMAIL_SUBJECT"], mail_dict["EMAIL_BODY"])

            if success:
                return "Check your mail/spam for code."

            return "Please try again."
