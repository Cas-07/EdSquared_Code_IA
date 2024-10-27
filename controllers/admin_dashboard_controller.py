from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.metrics import dp
from models.admin_model import Admin
from kivymd.uix.button import MDRoundFlatButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.boxlayout import BoxLayout
from models.session_manager_model import SessionManager

KV = """<CustomLayoutA>:
    orientation: "vertical"
    spacing: "12dp"
    size_hint_y : None
    padding: "10dp"
    height: "160dp"

    GridLayout:
        cols: 1
        spacing: dp(10)
        size_hint_y: None
        height: dp(140)
        pos_hint: {'center_x': 0.5}

        MDRaisedButton:
            text: "Sort by Last Name"
            theme_text_color: "Custom"
            md_bg_color: (0.6667, 0.4196, 0.7765, 1)
            size_hint: 1, None
            height: dp(20)
            font_name: 'utils/font/GalanoGrotesqueAltMedium.ttf'
            on_release: app.root.current_screen.admin_dashboard("LAST_NAME")

        MDRaisedButton:
            text: "Remove Student"
            theme_text_color: "Custom"
            md_bg_color: (0.6667, 0.4196, 0.7765, 1)
            size_hint: 1, None
            height: dp(20)
            font_name: 'utils/font/GalanoGrotesqueAltMedium.ttf'
            on_release: app.root.current_screen.go_to_page('admin_remove_student_view')

        MDRaisedButton:
            text: "Logout"
            theme_text_color: "Custom"
            md_bg_color: (0.6667, 0.4196, 0.7765, 1)
            size_hint: 1, None
            height: dp(20)
            font_name: 'utils/font/GalanoGrotesqueAltMedium.ttf'
            on_release: app.root.current_screen.logout()
"""

class CustomLayoutA(BoxLayout):
    pass

Builder.load_file('views/admin_dashboard_view.kv')

class AdminDashboardView(Screen):
    dialogA = None
    Builder.load_string(KV)
    def on_enter(self):
        self.ed_squared_app = App.get_running_app()
        self.admin_obj = self.ed_squared_app.current_user_obj
        self.ids.students_grid.clear_widgets()
        self.admin_dashboard(None)
        if self.dialogA:
            self.dialogA.dismiss()
        self.dialogA = None
        # return Builder.load_string(KV)

    def admin_dashboard(self, sorted_by):
        # Displays all the respective students for that admin/tutor, if no one is presented, displays an information message to send them their code
        self.ids.students_grid.clear_widgets()
        self.ids.no_students_info.text = ''
        student_details = self.admin_obj.fetch_students_summary(sorted_by)
        if student_details:
            for student_row in student_details:
                self.add_student_row(student_row["ID"], student_row["FIRST_NAME"], student_row["LAST_NAME"], student_row["EMAIL"])
        else:
            print("No Student registered with the tutor.")
            if not self.admin_obj.code:
                self.get_tutor_code()
            info_text = f"It seems like you haven't added any students yet! Send them this code: {self.admin_obj.code} so they can register, and they will be displayed here. To learn more about the app and how to use it, please refer to this [ref=website][color=#2e2eb3][u]support page.[/u][/color][/ref]"
            self.ids.no_students_info.text = info_text
            self.ids.no_students_info.height = dp(120)

    def get_tutor_code(self):
        # Allows tutor to get their tutor code anytime (by clicking the button)
        if self.admin_obj.code:
            tutor_code = self.admin_obj.code
        else:
            tutor_code = self.admin_obj.get_code()

        if tutor_code:
            if self.ids.tutor_code_display.text == 'Get Code':
                self.ids.tutor_code_display.text = tutor_code
            else:
                self.ids.tutor_code_display.text = 'Get Code'

    def add_student_row(self, student_id, first_name, last_name, student_mail):
        # Displays student with their first name, last name, and a button to redirect to the screen which displays the related details/operations for that student
        first_name_label = Label(text=first_name, color=(1, 1, 1, 1), halign='center', valign='middle', text_size=(dp(100), None), font_size='19sp')
        self.ids.students_grid.add_widget(first_name_label)
        last_name_label = Label(text=last_name, color=(1, 1, 1, 1), halign='center', valign='middle', text_size=(dp(100), None), font_size='19sp')
        self.ids.students_grid.add_widget(last_name_label)
        view_button = MDRoundFlatButton(text='View', md_bg_color=(0.6667, 0.4196, 0.7765, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5}, line_color=(1,1,1,1), text_color=(1,1,1,1), font_size='19sp')
        # On click view button event, callbacks to the view student grades screen, passing all the necessary parameters related to the student
        view_button.bind(on_release=lambda instance, name=first_name: self.view_student_grades(student_id, first_name, last_name, student_mail))
        self.ids.students_grid.add_widget(view_button)

    def view_student_grades(self, student_id, first_name, last_name, student_mail):
        self.manager.get_screen('student_detail_view').load_student_detail(student_id, first_name, last_name, student_mail)
        self.manager.transition = SlideTransition(direction='left')
        self.manager.change_screen('student_detail_view')

    def go_to_page(self, screen_name):
        if self.dialogA:
            self.dialogA.dismiss()
            self.dialogA = None
        if screen_name == "admin_dashboard_view":
            self.manager.transition = SlideTransition(direction='right')
            self.manager.change_screen(screen_name)

        else:
            self.manager.get_screen(screen_name).on_enter()
            self.manager.transition = SlideTransition(direction='left')
            self.manager.change_screen(screen_name)


    def show_menu(self):
        if self.dialogA:
            self.dialogA.dismiss()
            self.dialogA = None
        self.dialogA = MDDialog(
            title="Menu",
            type="custom",
            content_cls=CustomLayoutA(),
        )
        self.dialogA.open()

    def logout(self):
        if self.dialogA:
            self.dialogA.dismiss()
            self.dialogA = None
        self.admin_obj.db_conn.close_conn()
        self.ed_squared_app.session_manager.logout()
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = "login_view"
