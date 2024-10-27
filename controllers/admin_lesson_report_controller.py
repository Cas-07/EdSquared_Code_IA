from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from utils.macros import API_KEY, API_URL
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.boxlayout import MDBoxLayout
from models.admin_model import Admin
from models.session_manager_model import SessionManager
import datetime
from concurrent.futures import ThreadPoolExecutor
from kivy.clock import mainthread, Clock
from kivy.metrics import dp
import requests

Builder.load_file('views/admin_lesson_report_view.kv')

class AdminLessonReportView(Screen):
    def on_load(self, student_metadata):
        self.ed_squared_app = App.get_running_app()
        self.admin_obj = self.ed_squared_app.current_user_obj
        self.executor = ThreadPoolExecutor(max_workers=1) # Executer object with one worker thread
        self.metadata = student_metadata
        self.ids.student_name.text = f"{self.metadata['first_name']} {self.metadata['last_name']}"
        self.ids.subject_name.text = self.metadata["subject_name"]

    def save_lesson_report(self):
        student_id = self.metadata["student_id"]
        subject_id = self.metadata["subject_id"]
        if self.ids.date_picker.text != "Select Date":
            date = datetime.datetime.strptime(self.ids.date_picker.text, "%d-%m-%Y")
            sub_topic = self.ids.subtopic_input.text
            report_content = self.ids.report_input.text
            homework_var = self.ids.homework_toggle.active
            if self.ids.lesson_link_input.text != '':
                lesson_link = self.ids.lesson_link_input.text
            else:
                lesson_link = None
            if sub_topic != "" and report_content != "":
                self.admin_obj.save_lesson_report(student_id, subject_id, sub_topic, report_content, lesson_link, date, homework_var)
                self.ids.date_picker.text = "Select Date"
                self.ids.subtopic_input.text = ""
                self.ids.report_input.text = ""
                self.ids.lesson_link_input.text = ""
                self.ids.homework_toggle.active = False

    def homework_toggle(self, active):
        if active:
            self.ids.toggle_text.text = "Homework is set"
        else:
            self.ids.toggle_text.text = "Homework not set"

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)
        value = value.strftime('%d-%m-%Y')
        self.ids.date_picker.text = str(value)

    def on_cancel(self, instance, value):
        print("Date Picker Closed.")

    def chatgpt_api_query(self, report_keyword):
        # Sends a request to the OpenAI ChatGPT API to generate a lesson report based on the provided
        # report keyword and subtopic.
        sub_topic = self.ids.subtopic_input.text

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {API_KEY}',
        }

        data = {
            'model': 'gpt-3.5-turbo',
            'messages': [
                {'role': 'system', 'content': 'You are a knowledgeable tutor providing lesson report.'},
                {'role': 'user', 'content': f'Report must be around tutor keywords for lesson report: {report_keyword} if present to make your response more specific. Subtopic for lesson report: {sub_topic} for subject: {self.metadata["subject_name"]}  to provide lesson report. Lesson report should be strictly no more than 500 characters. Write lesson report.'}
            ],
        }

        response = requests.post(API_URL, headers=headers, json=data)

        if response.status_code == 200:
            response_data = response.json()
            assistant_reply = response_data['choices'][0]['message']['content']
            return assistant_reply
        else:
            return 'Error generating lesson report. Please try again.'

    def load_data(self):
        report_keyword = self.ids.report_input.text
        self.ids.report_input.text = ""
        spinner = self.ids.spinner
        spinner.active = True
        spinner.size = (dp(30), dp(30))
        #Submit API query to thread pool and schedule UI update with the result once the task is complete
        future = self.executor.submit(self.chatgpt_api_query, report_keyword)
        future.add_done_callback(lambda future: Clock.schedule_once(lambda dt: self.data_loaded(future.result()), 0))

    @mainthread # Mainthread decorator to ensure the following method is executed on the main UI thread,
                # crucial for updating UI elements from background threads.
    def data_loaded(self, data, *args):
        spinner = self.ids.spinner
        spinner.active = False
        spinner.size = (dp(0), dp(0))
        self.ids.report_input.text = data

    def go_to_page(self, screen_name):
        self.manager.get_screen(screen_name).on_load(self.metadata)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.change_screen(screen_name)
