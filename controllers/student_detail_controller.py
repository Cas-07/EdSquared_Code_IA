from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.metrics import dp
from models.admin_model import Admin
from helpers.email_helper import get_homework_mail_content, send_mail
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.factory import Factory
import threading
from kivy.lang import Builder
from kivymd.app import MDApp

KV = """<CustomLayoutB>:
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
            text: "Add Grade"
            theme_text_color: "Custom"
            md_bg_color: (0.6667, 0.4196, 0.7765, 1)
            size_hint_x: 1
            size_hint_y: None
            height: dp(50)
            font_name: 'utils/font/GalanoGrotesqueAltMedium.ttf'
            on_release: app.root.current_screen.go_to_page('admin_add_grades_view')

        MDRaisedButton:
            text: "Edit Subject"
            theme_text_color: "Custom"
            md_bg_color: (0.6667, 0.4196, 0.7765, 1)
            size_hint_x: 1
            size_hint_y: None
            height: dp(50)
            font_name: 'utils/font/GalanoGrotesqueAltMedium.ttf'
            on_release: app.root.current_screen.go_to_page('admin_edit_subjects_view')

        MDRaisedButton:
            text: "Homework"
            theme_text_color: "Custom"
            md_bg_color: (0.6667, 0.4196, 0.7765, 1)
            size_hint_x: 1
            size_hint_y: None
            height: dp(50)
            font_name: 'utils/font/GalanoGrotesqueAltMedium.ttf'
            on_release: app.root.current_screen.go_to_page('admin_homework_view')

        # MDRaisedButton:
        #     text: "Dashboard"
        #     md_bg_color: (0.6667, 0.4196, 0.7765, 1)
        #     theme_text_color: "Custom"
        #     size_hint_x: 1
        #     size_hint_y: None
        #     height: dp(50)
        #     font_name: 'utils/font/GalanoGrotesqueAltMedium.ttf'
        #     on_release: app.root.current_screen.go_to_page('admin_dashboard_view')
"""

class CustomLayoutB(BoxLayout):
    pass

Builder.load_file('views/student_detail_view.kv')

class StudentDetailView(Screen):
    dialogB = None
    Builder.load_string(KV)
    def on_enter(self):
        self.ed_squared_app = App.get_running_app()
        self.admin_obj = self.ed_squared_app.current_user_obj
        self.ids.subjects_grid.clear_widgets()
        self.set_student_details()
        if self.dialogB:
            self.dialogB.dismiss()
        self.dialogB = None
        # return Builder.load_string(KV)

    def load_student_detail(self, student_id, first_name, last_name, student_mail):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.student_mail = student_mail
        self.metadata = {"student_id":self.student_id, "student_mail":self.student_mail, "first_name":self.first_name, "last_name":self.last_name}


    def set_student_details(self):
        self.ids.student_name.text = f"{self.first_name} {self.last_name}"
        grade_summary = self.admin_obj.fetch_details_by_student_id(self.student_id)
        if grade_summary:
            for summary in grade_summary:
                self.add_subjects_row(summary["ID"], summary["NAME"], summary["EXAM_TYPE"], summary["GRADE"], summary["COLOUR"])

    # def set_homework_status(self):
    #     last_homework = self.admin_obj.fetch_homework(self.student_id, 1)
    #     if last_homework:
    #         self.ids.homework_text.text = last_homework["HOMEWORK"]
    #         if last_homework["STATUS"]:
    #             self.ids.homework_header.color = [0, 1, 0, 1]
    #             self.ids.homework_header.text = "Homework: Completed"
    #         else:
    #             self.ids.homework_header.color = [1, 0, 0, 1]
    #             self.ids.homework_header.text = "Homework: Not Completed"
    #     else:
    #         self.ids.homework_text.text = ''
    #         self.ids.homework_header.color = [1, 1, 1, 1]
    #         self.ids.homework_header.text = "Homework: Not Assigned"


    def hex_to_rgba(self, hex_color):
        hex_color = hex_color.lstrip('#')

        if len(hex_color) != 6:
            raise ValueError("Hex color must be 6 characters long.")

        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)

        a = 1.0

        return (r / 255.0, g / 255.0, b / 255.0, a)

    def add_subjects_row(self, subject_id, subject_name, exam_type, grade, colour):
        subject_colour = self.hex_to_rgba(colour)
        if len(subject_name) > 12:
            subject_label = MDRoundFlatButton(text=subject_name[0:11], md_bg_color=subject_colour, line_color=(1, 1, 1, 1), text_color=(1,1,1,1), font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        else:
            subject_label = MDRoundFlatButton(text=subject_name, md_bg_color=subject_colour, line_color=(1, 1, 1, 1), text_color=(1,1,1,1), font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        # exam_type_label = Label(text=str(exam_type), color=(1,1,1,1), font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        grade_label = Label(text=str(grade), color=(1,1,1,1), font_name='utils/font/GalanoGrotesqueAltMedium.ttf')

        student_metadata = {"student_id":self.student_id, "student_mail":self.student_mail, "first_name":self.first_name, "last_name":self.last_name, "subject_id":subject_id, "subject_name":subject_name}
        grade_history_button = MDRoundFlatButton(text='Grade', md_bg_color=(0.6667, 0.4196, 0.7765, 1), line_color=(1, 1, 1, 1), text_color=(1,1,1,1), font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        grade_history_button.bind(on_release=lambda instance, name=student_metadata: self.view_subject_history(student_metadata))
        self.ids.subjects_grid.add_widget(subject_label)
        # self.ids.subjects_grid.add_widget(exam_type_label)
        self.ids.subjects_grid.add_widget(grade_label)
        # self.ids.subjects_grid.add_widget(lesson_report_button)
        self.ids.subjects_grid.add_widget(grade_history_button)

    def view_subject_history(self, student_metadata):
        self.manager.get_screen('subject_detail_view').load_subject_history(student_metadata)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.change_screen('subject_detail_view')

    def view_add_grades(self, student_metadata):
        self.manager.get_screen('admin_add_grades_view').on_enter(student_metadata)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.change_screen('admin_add_grades_view')

    def view_add_grades(self, student_metadata):
        self.manager.get_screen('admin_edit_subjects_view').on_enter(student_metadata)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.change_screen('admin_edit_subjects_view')

    def go_to_page(self, screen_name):
        if self.dialogB:
            self.dialogB.dismiss()
            self.dialogB = None
        if screen_name == "admin_dashboard_view":
            self.manager.transition = SlideTransition(direction='right')
            self.manager.change_screen(screen_name)
        else:
            self.manager.get_screen(screen_name).on_load(self.metadata)
            self.manager.transition = SlideTransition(direction='left')
            self.manager.change_screen(screen_name)


    def show_menu(self):
        if self.dialogB:
            self.dialogB.dismiss()
            self.dialogB = None
        self.dialogB = MDDialog(
            title="Menu",
            type="custom",
            content_cls=CustomLayoutB(),
        )
        self.dialogB.open()

    # def save_homework(self):
    #     homework_text = self.ids.homework_text.text
    #     if homework_text:
    #         if self.admin_obj.assign_homework(self.student_id, homework_text):
    #             self.set_homework_status()
    #             mail_dict = get_homework_mail_content(self.student_mail, self.first_name, self.last_name, self.ids.homework_text.text)
    #             threading.Thread(target=send_mail, args=(
    #                 mail_dict["SENDER_MAIL"],
    #                 mail_dict["RECEIVER_MAIL"],
    #                 mail_dict["EMAIL_SUBJECT"],
    #                 mail_dict["EMAIL_BODY"]
    #             )).start()
    #         else:
    #             print(f"Failed to save homework.")
    #     else:
    #         print(f"Homework field is empty.")
