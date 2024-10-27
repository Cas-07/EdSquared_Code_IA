from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.app import App
from models.student_model import Student
from kivymd.uix.button import MDRoundFlatButton

# Load the corresponding .kv file
Builder.load_file('views/student_grades_view.kv')

class StudentGradesView(Screen):
    def on_enter(self):
        self.ed_squared_app = App.get_running_app()
        self.student_obj = self.ed_squared_app.current_user_obj
        self.list_student_subjects()

    def list_student_subjects(self):
        self.ids.subjects_grid.clear_widgets()
        subjects = self.student_obj.list_student_subjects(self.student_obj.id)
        if subjects:
            for subject in subjects:
                self.add_subject_row(subject["ID"], subject["NAME"])

    def add_subject_row(self, subject_id, subject_name):
        if len(subject_name) > 26:
            subject_label = Label(text=subject_name[0:25], color=(1, 1, 1, 1), text_size=(self.width, None), halign='center', valign='middle', font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        else:
            subject_label = Label(text=subject_name, color=(1, 1, 1, 1), text_size=(self.width, None), halign='center', valign='middle', font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        view_lesson_report_button = MDRoundFlatButton(text='Lesson Reports', md_bg_color=(0.6667, 0.4196, 0.7765, 1), line_color=(1, 1, 1, 1), text_color=(1,1,1,1), size_hint_x=0.3, font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        view_lesson_report_button.bind(on_release=lambda instance, id=subject_id: self.view_subject_lesson_report(subject_id, subject_name))
        view_grade_button = MDRoundFlatButton(text='Grades', md_bg_color=(0.6667, 0.4196, 0.7765, 1), line_color=(1, 1, 1, 1), text_color=(1,1,1,1), size_hint_x=0.3, font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        view_grade_button.bind(on_release=lambda instance, id=subject_id: self.view_subject_grades(subject_id, subject_name))

        subject_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))

        self.ids.subjects_grid.add_widget(subject_label)
        self.ids.subjects_grid.add_widget(view_lesson_report_button)
        self.ids.subjects_grid.add_widget(view_grade_button)

    def view_subject_lesson_report(self, subject_id, subject_name):
        self.manager.get_screen('student_lesson_report_view').load_lesson_reports(subject_id, subject_name)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.change_screen('student_lesson_report_view')

    def view_subject_grades(self, subject_id, subject_name):
        self.manager.get_screen('subject_grades_view').load_subject_grades(subject_id, subject_name)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.change_screen('subject_grades_view')
