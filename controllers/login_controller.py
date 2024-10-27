# All the necessary imports related to UI and other functionalities assisting user login
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.app import App
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from utils.macros import EMAIL_PATTERN
from models.student_model import Student
from models.admin_model import Admin
import re

# Loading the .kv file for login
Builder.load_file('views/login_view.kv')

class LoginView(Screen): # Inheriting class screen to access the login UI
    def on_enter(self): # Gets triggered as soon as the screen loads/opens
        self.ed_squared_app = App.get_running_app() # Fetching the current instance of the running application

    def login(self, email, password): # Gets triggered as soon as the user clicks on the login button
        if not email or not password:
            self.ids.login_message.text = 'All fields are required.'
            return

        user = "STUDENT"
        if self.ids.admin_checkbox.active: # If the admin/tutor checkbox is selected, the user type changes to admin
            user = "ADMIN"
        email = email.strip().upper() # Sanitizes email field
        if user == "STUDENT": # If user is a student, authenticate using a student object
            student_obj = Student()
            response = student_obj.authenticate_student(email, password)
        elif user == "ADMIN": # If user is an admin, authenticate using an admin object
            admin_obj = Admin()
            response = admin_obj.authenticate_admin(email, password)
        # If authentication is successfull, set all the fields to empty,
        # create a session object, update the session.json file,
        # and redirects to the respective user dashboard (student or admin)
        # else displays an error authenticating message
        if response:
            self.ids.email_input.text = ''
            self.ids.password_input.text = ''
            self.ids.admin_checkbox.active = False
            self.ed_squared_app.session_manager.login(response)
            print(f"{user.capitalize()}: {email} LoggedIn.")
            self.ed_squared_app.current_user_obj = self.ed_squared_app.session_manager.get_current_user()
            self.ed_squared_app.current_user_type = self.ed_squared_app.session_manager.get_current_user_type()
            self.manager.transition = SlideTransition(direction='left')
            self.manager.current = f'{user.lower()}_dashboard_view'
        else:
            print(f"Error Authenticating {user.capitalize()}: {email}")
            self.ids.login_message.text = f"Error Authenticating {user.capitalize()}: {email}"
