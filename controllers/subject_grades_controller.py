from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp
from models.student_model import Student

# Load the corresponding .kv file
Builder.load_file('views/subject_grades_view.kv')

class SubjectGradesView(Screen):
    def load_subject_grades(self, subject_id, subject_name):
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.ids.grades_grid.clear_widgets()
        self.ids.subject_label.text = self.subject_name
        self.ed_squared_app = App.get_running_app()
        self.student_obj = self.ed_squared_app.current_user_obj
        self.display_subject_grades()

    def display_subject_grades(self):
        grade_history = self.student_obj.fetch_grades_by_subject(self.student_obj.id, self.subject_id)
        if grade_history:
            for history in grade_history:
                self.add_grades_row(history["ADDED_AT"].date(), history["EXAM_TYPE"], history["GRADE"])


    def add_grades_row(self, date, exam_type, grade):
        date_label = Label(text=str(date.strftime('%d-%m-%Y')), color=(1, 1, 1, 1), font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        exam_type_label = Label(text=str(exam_type), color=(1, 1, 1, 1), halign='center', valign='middle', text_size=(dp(120), None), font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        grade_label = Label(text=grade, color=(1, 1, 1, 1), font_name='utils/font/GalanoGrotesqueAltMedium.ttf')

        self.ids.grades_grid.add_widget(date_label)
        self.ids.grades_grid.add_widget(exam_type_label)
        self.ids.grades_grid.add_widget(grade_label)
