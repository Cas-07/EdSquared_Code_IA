from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.app import App
from models.student_model import Student
from models.session_manager_model import SessionManager

Builder.load_file('views/student_dashboard_view.kv')

class StudentDashboardView(Screen):
    def on_enter(self):
        self.ed_squared_app = App.get_running_app()
        self.student_obj = self.ed_squared_app.current_user_obj

    def logout(self):
        self.student_obj.db_conn.close_conn()
        self.ed_squared_app.session_manager.logout()
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = "login_view"
