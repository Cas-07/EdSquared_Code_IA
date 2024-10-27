from kivy.uix.screenmanager import Screen
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivymd.uix.textfield import MDTextField
from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp
from models.student_model import Student
from datetime import datetime

Builder.load_file('views/student_add_grades_view.kv')

class StudentAddGradesView(Screen):
    added_grades = []
    def on_enter(self):
        self.ed_squared_app = App.get_running_app()
        self.user_obj = self.ed_squared_app.current_user_obj

    def add_grades_row(self):
        # Adds a new row to the grades grid with a subject dropdown, and empty fields for exam type and grade.
        # Each widget is bound to handlers to capture user interactions, updating the added_grades list to
        # track the selected subject and its corresponding exam type and grade.
        subject_spinner = Spinner(
            text='Select Subject',
            values=self.get_subject_names(),
            background_color=(1, 1, 1, 1),
            color=(0, 0, 0, 1),
            size_hint_y=None,
            size_hint_x = 0.4,
            height=dp(40)
        )
        subject_spinner.bind(text=self.on_spinner_select)

        exam_type_box = BoxLayout(orientation='horizontal', size_hint_y=None, size_hint_x=0.4, height=dp(40))
        exam_type_input = MDTextField(multiline=False, mode="round", background_color=(1, 1, 1, 1), size_hint_x=0.2, foreground_color=(0, 0, 0, 1), size_hint_y=None, height=dp(30))
        exam_type_input.bind(text=self.update_added_grades)
        exam_type_box.add_widget(exam_type_input)

        grade_input = MDTextField(multiline=False, mode="round", background_color=(1, 1, 1, 1), size_hint_x=0.2, foreground_color=(0, 0, 0, 1), size_hint_y=None, height=dp(30))
        grade_input.bind(text=self.update_added_grades)

        self.ids.grades_grid.add_widget(subject_spinner)
        self.ids.grades_grid.add_widget(exam_type_box)
        self.ids.grades_grid.add_widget(grade_input)

        self.added_grades.append([subject_spinner, exam_type_input, grade_input])

    def on_spinner_select(self, spinner, text):
        print(f'Selected subject: {text}')

    def get_subject_names(self):
        subjects = self.user_obj.list_student_subjects(self.user_obj.id)
        if subjects:
            return [subject["NAME"] for subject in subjects]
        else:
            return ["None"]

    def update_added_grades(self, *args):
        updated_grades = []
        for spinner, exam_type_input, grade_input in self.added_grades:
            updated_grades.append([spinner, exam_type_input, grade_input])
        self.added_grades = updated_grades
        print("Updated grades:", self.added_grades)
###
    def save_grades(self):
        # Handles the saving of student grades for the current day.
        # It checks if there are existing grade records for the student and specific subjects on the current date.
        # If a record already exists for a subject, it updates the grade entry.
        # Else, it adds a new grade record for that subject.
        # The method tracks if any database operations (insert or update) are performed and clears the input fields upon completion.
        db_operation = False
        self.update_added_grades() # Ensure the latest grade entries are collected
        curr_date = datetime.now().date()
        todays_entry = self.user_obj.check_grades_date(self.user_obj.id, curr_date)
        added_sub_ids = []
        if todays_entry:
            added_sub_ids = [element["SUBJECT_ID"] for element in todays_entry]
        for grade in self.added_grades:
            sub_id = self.user_obj.fetch_subject_id(grade[0].text)
            print(self.user_obj.id, grade[0].text, grade[1].text, grade[2].text)
            print(sub_id, "----", added_sub_ids)
            if sub_id and sub_id["ID"] in added_sub_ids:
                if grade[0].text != "Select Subject" and grade[2].text != '':
                    self.user_obj.update_grades(self.user_obj.id, sub_id["ID"], grade[1].text, grade[2].text, curr_date)
                    db_operation = True
            else:
                if grade[0].text != "Select Subject" and grade[2].text != '':
                    self.user_obj.upload_grades(self.user_obj.id, grade[0].text, grade[1].text, grade[2].text)
                    db_operation = True

        if db_operation:
            self.added_grades = []
            self.ids.grades_grid.clear_widgets()
