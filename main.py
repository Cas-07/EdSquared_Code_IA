# mysql --user avnadmin --password=AVNS_DCOxF4PB5lWmY5kYj4b --host edsquared-db-eagereverest-04cd.h.aivencloud.com --port 12098 defaultdb

from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.core.window import Window
from kivy.metrics import dp
from kivy import platform
from models.session_manager_model import SessionManager
from controllers.contact_us_controller import ContactUsView
from controllers.reset_password_controller import ResetPasswordView
from controllers.login_controller import LoginView
from controllers.registration_controller import RegistrationView
from controllers.student_dashboard_controller import StudentDashboardView
from controllers.student_grades_controller import StudentGradesView
from controllers.subject_grades_controller import SubjectGradesView
from controllers.student_add_grades_controller import StudentAddGradesView
from controllers.student_feedback_controller import StudentFeedbackView
from controllers.student_homework_controller import StudentHomeworkView
from controllers.student_edit_subjects_controller import StudentEditSubjectsView
from controllers.student_lesson_report_controller import StudentLessonReportView
from controllers.student_add_admin_controller import StudentAddAdminView
from controllers.admin_dashboard_controller import AdminDashboardView
from controllers.student_detail_controller import StudentDetailView
from controllers.subject_detail_controller import SubjectDetailView
from controllers.admin_lesson_report_controller import AdminLessonReportView
from controllers.admin_lesson_report_history_controller import AdminLessonReportHistoryView
from controllers.admin_remove_student_controller import AdminRemoveStudentView
from controllers.admin_add_grades_controller import AdminAddGradesView
from controllers.admin_edit_subjects_controller import AdminEditSubjectsView
from controllers.admin_homework_controller import AdminHomeworkView
from controllers.admin_feedback_controller import AdminFeedbackView

def set_screen_size():
    if platform == 'android':
        print("Running on Android")
    elif platform == 'ios':
        screen_width, screen_height = Window.size

        if screen_width == dp(375) and screen_height == dp(812):
            print("Detected iPhone X/XS/11 Pro/12 mini/13 mini")
            Window.size = (dp(375), dp(812))
        elif screen_width == dp(414) and screen_height == dp(896):
            print("Detected iPhone XR/11/11 Pro Max/XS Max")
            Window.size = (dp(414), dp(896))
        elif screen_width == dp(390) and screen_height == dp(844):
            print("Detected iPhone 12/12 Pro/13/13 Pro/14")
            Window.size = (dp(390), dp(844))
        elif screen_width == dp(428) and screen_height == dp(926):
            print("Detected iPhone 12 Pro Max/13 Pro Max/14 Plus")
            Window.size = (dp(428), dp(926))
        elif screen_width == dp(393) and screen_height == dp(852):
            print("Detected iPhone 14 Pro")
            Window.size = (dp(393), dp(852))
        elif screen_width == dp(430) and screen_height == dp(932):
            print("Detected iPhone 14 Pro Max")
            Window.size = (dp(430), dp(932))
        else:
            print("Default iPhone screen size")
            Window.size = (dp(393), dp(852))
    else:
        print("Running on Desktop or other platform")
        Window.size = (dp(430), dp(932))

set_screen_size()

class CustomScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen_history = []
        self.is_transitioning = False  # Add this flag to manage transitions

    def change_screen(self, screen_name):
        if not self.screen_history or self.screen_history[-1] != self.current:
            print(f"Adding {self.current} to history")
            if self.current != "login_view" and self.current != "registration_view":
                self.screen_history.append(self.current)

        print(f"Switching to {screen_name}")
        self.current = screen_name

    def go_back(self):
        if self.current in ["login_view", "registration_view", "reset_password_view", "admin_dashboard_view", "student_dashboard_view"]:
            print("Can't Swipe")
            return
        if self.screen_history and not self.is_transitioning:
            previous_screen = self.screen_history.pop()
            print(f"Going back to {previous_screen}")
            self.transition = SlideTransition(direction='right')
            self.is_transitioning = True
            self.current = previous_screen
            self.on_transition_complete()
        elif not self.screen_history:
            print("No more screens in history")

    def on_touch_move(self, touch):
        if not self.is_transitioning:
            if touch.dx > 50:
                print("Right swipe detected")
                self.go_back()
            elif touch.dx < -50:
                print("Left swipe detected")
        return super().on_touch_move(touch)

    def on_transition_complete(self, *args):
        print("Transition completed")
        self.is_transitioning = False  # Transition is done, allow new swipes



class EdSquaredApp(MDApp):
    def build(self):
        self.session_manager = SessionManager()
        self.current_user_obj = self.session_manager.get_current_user()
        self.current_user_type = self.session_manager.get_current_user_type()
        sm = CustomScreenManager()
        sm.add_widget(LoginView(name='login_view'))
        sm.add_widget(RegistrationView(name='registration_view'))
        sm.add_widget(ContactUsView(name='contact_us_view'))
        sm.add_widget(ResetPasswordView(name='reset_password_view'))
        # student screens
        sm.add_widget(StudentDashboardView(name='student_dashboard_view'))
        sm.add_widget(StudentGradesView(name='student_grades_view'))
        sm.add_widget(SubjectGradesView(name='subject_grades_view'))
        sm.add_widget(StudentAddGradesView(name='student_add_grades_view'))
        sm.add_widget(StudentFeedbackView(name='student_feedback_view'))
        sm.add_widget(StudentHomeworkView(name='student_homework_view'))
        sm.add_widget(StudentEditSubjectsView(name='student_edit_subjects_view'))
        sm.add_widget(StudentLessonReportView(name='student_lesson_report_view'))
        sm.add_widget(StudentAddAdminView(name='student_add_admin_view'))
        ## admin screens
        sm.add_widget(AdminDashboardView(name='admin_dashboard_view'))
        sm.add_widget(StudentDetailView(name='student_detail_view'))
        sm.add_widget(SubjectDetailView(name='subject_detail_view'))
        sm.add_widget(AdminLessonReportView(name='admin_lesson_report_view'))
        sm.add_widget(AdminLessonReportHistoryView(name="admin_lesson_report_history_view"))
        sm.add_widget(AdminRemoveStudentView(name='admin_remove_student_view'))
        sm.add_widget(AdminAddGradesView(name='admin_add_grades_view'))
        sm.add_widget(AdminEditSubjectsView(name='admin_edit_subjects_view'))
        sm.add_widget(AdminHomeworkView(name='admin_homework_view'))
        sm.add_widget(AdminFeedbackView(name='admin_feedback_view'))


        if self.current_user_obj:
            if self.current_user_type == "Student":
                sm.change_screen("student_dashboard_view")
            elif self.current_user_type == "Admin":
                sm.change_screen("admin_dashboard_view")
        else:
            sm.current = "login_view"

        return sm

if __name__ == '__main__':
    EdSquaredApp().run()
