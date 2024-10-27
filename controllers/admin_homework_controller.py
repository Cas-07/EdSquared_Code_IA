from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.metrics import dp
from models.admin_model import Admin
from helpers.email_helper import get_homework_mail_content, send_mail
from kivymd.uix.button import MDRoundFlatButton
import threading

Builder.load_file('views/admin_homework_view.kv')

class AdminHomeworkView(Screen):
    student_metadata = None
    def on_enter(self):
        self.ed_squared_app = App.get_running_app()
        self.admin_obj = self.ed_squared_app.current_user_obj
        self.set_homework_status()

    def on_load(self, student_metadata):
        self.student_metadata = student_metadata
        self.ids.student_name.text = f"{self.student_metadata['first_name']} {self.student_metadata['last_name']}"

    def set_homework_status(self):
        last_homework = self.admin_obj.fetch_homework(self.student_metadata['student_id'], 1)
        if last_homework:
            self.ids.homework_text.text = last_homework["HOMEWORK"]
            if last_homework["STATUS"]:
                self.ids.homework_header.color = [0, 1, 0, 1]
                self.ids.homework_header.text = "Homework: Completed"
            else:
                self.ids.homework_header.color = [1, 0, 0, 1]
                self.ids.homework_header.text = "Homework: Not Completed"
        else:
            self.ids.homework_text.text = ''
            self.ids.homework_header.color = [1, 1, 1, 1]
            self.ids.homework_header.text = "Homework: Not Assigned"

    def save_homework(self):
        homework_text = self.ids.homework_text.text
        if homework_text:
            print("poke", homework_text, self.student_metadata['student_id'])
            if self.admin_obj.assign_homework(self.student_metadata['student_id'], homework_text):
                self.set_homework_status()
                mail_dict = get_homework_mail_content(self.student_metadata['student_mail'], self.student_metadata['first_name'], self.student_metadata['last_name'], self.ids.homework_text.text)
                threading.Thread(target=send_mail, args=(
                    mail_dict["SENDER_MAIL"],
                    mail_dict["RECEIVER_MAIL"],
                    mail_dict["EMAIL_SUBJECT"],
                    mail_dict["EMAIL_BODY"]
                )).start()
            else:
                print(f"Failed to save homework.")
        else:
            print(f"Homework field is empty.")
