from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp
from kivymd.uix.textfield import MDTextField
from models.student_model import Student

Builder.load_file('views/student_feedback_view.kv')

class StudentFeedbackView(Screen):
    def on_enter(self):
        self.ed_squared_app = App.get_running_app()
        self.student_obj = self.ed_squared_app.current_user_obj
        self.ids.feedback_grid.clear_widgets()
        self.student_feedback()

    def student_feedback(self):
        recent_feedback = self.student_obj.fetch_feedback_all_subjects(self.student_obj.id)
        if recent_feedback:
            for feedback in recent_feedback:
                self.add_feedback_widgets(feedback["NAME"], feedback["FEEDBACK_TEXT"])

    def add_feedback_widgets(self, subject_name, feedback_text):
        subject_label = Label(text=subject_name, color=(1, 1, 1, 1), height=dp(30))
        feedback_box = MDTextField(text=feedback_text, mode="fill", multiline=True, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1), size_hint_y=None, height=dp(80), readonly=True)

        self.ids.feedback_grid.add_widget(subject_label)
        self.ids.feedback_grid.add_widget(feedback_box)
