from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.metrics import dp
from concurrent.futures import ThreadPoolExecutor
from kivy.clock import mainthread, Clock
from utils.macros import API_KEY, API_URL
import requests
from models.admin_model import Admin
from helpers.email_helper import get_homework_mail_content, send_mail
from kivymd.uix.button import MDRoundFlatButton

Builder.load_file('views/admin_feedback_view.kv')

class AdminFeedbackView(Screen):
    def on_load(self, student_metadata):
        self.ed_squared_app = App.get_running_app()
        self.admin_obj = self.ed_squared_app.current_user_obj
        self.metadata = student_metadata
        self.executor = ThreadPoolExecutor(max_workers=1)
        self.ids.student_name.text = f"{self.metadata['first_name']} {self.metadata['last_name']}"
        self.ids.subject_name.text = self.metadata['subject_name']
        self.set_feedback()

    def set_feedback(self):
        recent_feedback = self.admin_obj.fetch_recent_feedback(self.metadata["student_id"], self.metadata["subject_id"])
        if recent_feedback:
            self.ids.feedback_text.text = recent_feedback["FEEDBACK_TEXT"]
        else:
            self.ids.feedback_text.text = ""

    def save_feedback(self):
        subject_feedback = self.ids.feedback_text.text
        if subject_feedback:
            self.admin_obj.save_student_feedback(self.metadata["student_id"], self.metadata["subject_id"], subject_feedback)

    def chatgpt_api_query(self, feedback_keyword):
        grade_history = self.admin_obj.fetch_last_5_grades(self.metadata["student_id"], self.metadata["subject_id"])
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}',
        }

        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': 'You are a knowledgeable tutor providing constructive feedback.'},
                {'role': 'user', 'content': f'Must consider tutor keywords: {feedback_keyword} if present to make your response more specific. Use the following grades: {grade_history} for subject: {self.metadata["subject_name"]} and student: {self.metadata["first_name"]} to provide constructive feedback. Feedback should be strictly no more than 310 characters. Write feedback in second person as it is for the student'}
            ],
        }

        response = requests.post(API_URL, headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            assistant_reply = response_data['choices'][0]['message']['content']
            return assistant_reply
        else:
            return 'Error generating feedback. Please try again.'

    def load_data(self):
        feedback_keyword = self.ids.feedback_text.text
        self.ids.feedback_text.text = ""
        spinner = self.ids.spinner
        spinner.active = True
        spinner.size = (dp(40), dp(40))

        future = self.executor.submit(self.chatgpt_api_query, feedback_keyword)
        future.add_done_callback(lambda future: Clock.schedule_once(lambda dt: self.data_loaded(future.result()), 0))

    @mainthread
    def data_loaded(self, data, *args):
        spinner = self.ids.spinner
        spinner.active = False
        spinner.size = (dp(0), dp(0))
        self.ids.feedback_text.text = data
