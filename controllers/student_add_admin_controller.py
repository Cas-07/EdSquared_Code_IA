from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.metrics import dp
from models.admin_model import Admin
from kivymd.uix.button import MDRoundFlatButton
from models.session_manager_model import SessionManager

Builder.load_file('views/student_add_admin_view.kv')

class StudentAddAdminView(Screen):
    def on_enter(self):
        self.ed_squared_app = App.get_running_app()
        self.student_obj = self.ed_squared_app.current_user_obj
        self.ids.admin_grid.clear_widgets()
        self.fetch_related_admins()

    def fetch_related_admins(self):
        related_admins = self.student_obj.get_related_admins(self.student_obj.id)
        print(related_admins)
        if related_admins:
            for admin in related_admins:
                self.add_admin_row(f"{admin['FIRST_NAME']} {admin['LAST_NAME']}", admin["CODE"])

    def add_admin_row(self, admin_name, admin_code):
        admin_label = Label(text=f"{admin_name} ( {admin_code} )", color=(1, 1, 1, 1), text_size=(self.width, None), halign='center', valign='middle', font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        admin_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))

        self.ids.admin_grid.add_widget(admin_label)

    def add_admin(self, admin_code):
        if self.student_obj.add_admin(self.student_obj.id, admin_code):
            self.ids.admin_grid.clear_widgets()
            self.fetch_related_admins()
        else:
            print("hi")
            self.ids.screen_msg.text = 'Probably incorrect Admin Code. Try Again'

    def remove_admin(self, admin_code):
        if self.student_obj.remove_admin(self.student_obj.id, admin_code):
            self.ids.admin_grid.clear_widgets()
            self.fetch_related_admins()
        else:
            self.ids.screen_msg.text = 'Please try again or later'
