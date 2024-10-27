from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from models.student_model import Student
from datetime import datetime
from kivy.metrics import dp
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Ellipse
from concurrent.futures import ThreadPoolExecutor
from kivy.clock import mainthread, Clock
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

KV = """<CustomLayoutC>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y: None
    padding: "10dp"
    height: "160dp"

    GridLayout:
        cols: 2
        spacing: dp(10)
        size_hint_y: None
        height: dp(120)
        pos_hint: {'center_x': 0.5}

        MDRaisedButton:
            text: "View Report"
            theme_text_color: "Custom"
            md_bg_color: (0.6667, 0.4196, 0.7765, 1)
            size_hint_x: 1
            size_hint_y: None
            height: dp(50)
            font_name: 'utils/font/GalanoGrotesqueAltMedium.ttf'
            on_release: app.root.current_screen.go_to_page('admin_lesson_report_history_view')

        MDRaisedButton:
            text: "Add Report"
            theme_text_color: "Custom"
            md_bg_color: (0.6667, 0.4196, 0.7765, 1)
            size_hint_x: 1
            size_hint_y: None
            height: dp(50)
            font_name: 'utils/font/GalanoGrotesqueAltMedium.ttf'
            on_release: app.root.current_screen.go_to_page('admin_lesson_report_view')

        MDRaisedButton:
            text: "Feedback"
            theme_text_color: "Custom"
            md_bg_color: (0.6667, 0.4196, 0.7765, 1)
            size_hint_x: 1
            size_hint_y: None
            height: dp(50)
            font_name: 'utils/font/GalanoGrotesqueAltMedium.ttf'
            on_release: app.root.current_screen.go_to_page('admin_feedback_view')

        MDRaisedButton:
            text: "Add Grade"
            theme_text_color: "Custom"
            md_bg_color: (0.6667, 0.4196, 0.7765, 1)
            size_hint_x: 1
            size_hint_y: None
            height: dp(50)
            font_name: 'utils/font/GalanoGrotesqueAltMedium.ttf'
            on_release: app.root.current_screen.go_to_page('admin_add_grades_view')

        # MDRaisedButton:
        #     text: "Dashboard"
        #     theme_text_color: "Custom"
        #     md_bg_color: (0.6667, 0.4196, 0.7765, 1)
        #     size_hint_x: 1
        #     size_hint_y: None
        #     height: dp(50)
        #     font_name: 'utils/font/GalanoGrotesqueAltMedium.ttf'
        #     on_release: app.root.current_screen.go_to_page('admin_dashboard_view')
"""

class CustomLayoutC(BoxLayout):
    pass

Builder.load_file('views/subject_detail_view.kv')

class SubjectDetailView(Screen):
    dialogC = None
    Builder.load_string(KV)
    def on_enter(self):
        self.ed_squared_app = App.get_running_app()
        self.admin_obj = self.ed_squared_app.current_user_obj
        self.ids.grades_grid.clear_widgets()
        self.set_subject_details()
        if self.dialogC:
            self.dialogC.dismiss()
        self.dialogC = None
        # return Builder.load_string(KV)

    def load_subject_history(self, student_metadata):
        self.metadata = student_metadata
        # self.executor = ThreadPoolExecutor(max_workers=1)
        self.ids.student_name.text = f"{self.metadata['first_name']} {self.metadata['last_name']}"
        self.ids.subject_name.text = self.metadata["subject_name"]
        # self.set_feedback()

    # def set_feedback(self):
    #     recent_feedback = self.admin_obj.fetch_recent_feedback(self.metadata["student_id"], self.metadata["subject_id"])
    #     if recent_feedback:
    #         self.ids.feedback_text.text = recent_feedback["FEEDBACK_TEXT"]
    #     else:
    #         self.ids.feedback_text.text = ""

    def set_subject_details(self):
        subject_grade_history = self.admin_obj.fetch_subject_grade_history(self.metadata["student_id"], self.metadata["subject_id"])
        if subject_grade_history:
            for history in subject_grade_history:
                self.add_grades_row(history["ADDED_AT"], history["EXAM_TYPE"], history["GRADE"])

    def add_grades_row(self, date, exam_type, grade):
        date_label = Label(text=str(date.date().strftime('%d-%m-%Y')), color=(1, 1, 1, 1), halign='center', valign='middle', text_size=(dp(100), None), font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        self.ids.grades_grid.add_widget(date_label)
        exam_type_label = Label(text=str(exam_type), color=(1, 1, 1, 1), halign='center', valign='middle', text_size=(dp(120), None), font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        self.ids.grades_grid.add_widget(exam_type_label)
        grade_label = Label(text=str(grade), color=(1, 1, 1, 1), halign='center', valign='middle', text_size=(dp(100), None), font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        self.ids.grades_grid.add_widget(grade_label)

    def go_to_page(self, screen_name):
        if self.dialogC:
            self.dialogC.dismiss()
            self.dialogC = None
        if screen_name == "admin_dashboard_view":
            self.manager.transition = SlideTransition(direction='right')
            self.manager.change_screen(screen_name)
        else:
            self.manager.get_screen(screen_name).on_load(self.metadata)
            self.manager.transition = SlideTransition(direction='left')
            self.manager.change_screen(screen_name)

    def show_menu(self):
        if self.dialogC:
            self.dialogC.dismiss()
            self.dialogC = None
        self.dialogC = MDDialog(
            title="Menu",
            type="custom",
            content_cls=CustomLayoutC(),
        )
        self.dialogC.open()

    def edit_lesson_report(self):
        self.manager.get_screen('admin_lesson_report_view').load_edit_lesson_report_view(self.metadata)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.change_screen('admin_lesson_report_view')
