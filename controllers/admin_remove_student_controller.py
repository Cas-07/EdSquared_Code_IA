from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.app import App
from kivy.metrics import dp
from models.admin_model import Admin
from kivymd.uix.button import MDRoundFlatButton
from models.session_manager_model import SessionManager

Builder.load_file('views/admin_remove_student_view.kv')

class AdminRemoveStudentView(Screen):

    student_id = None

    def on_enter(self):
        self.ed_squared_app = App.get_running_app()
        self.admin_obj = self.ed_squared_app.current_user_obj

    def update_recycleview_height(self, search_result):
        if search_result:
            self.ids.results_view.height = dp(100)
        else:
            print("pokemon", search_result)
            self.ids.results_view.height = 0

    def remove_student(self, student_email):
        self.admin_obj.remove_student(self.admin_obj.id, student_email)
        print(f"Deleted student: {student_email}")
        self.ids.student_email_box.text = ""
        self.ids.search_box.text = ""

    def search_student_keyword(self, keyword):
        self.ids.results_view.data = []
        self.update_recycleview_height(keyword)
        if keyword:
            keyword = keyword.strip().upper()
            response = self.admin_obj.search_student_by_keyword(self.admin_obj.id, keyword)
            search_result = []
            if response:
                for student in response:
                    search_result.append((student["ID"], student["EMAIL"], f"{student['FIRST_NAME']} {student['LAST_NAME']}"))
                print(search_result)
                self.update_search_results(search_result)
            else:
                self.update_recycleview_height(keyword)

    def update_search_results(self, search_result):
        self.ids.results_view.data = [{'stu_id': stu_id, 'text': f'{stu_name} ({stu_mail})', 'on_select': self.select_student} for stu_id, stu_mail, stu_name in search_result]

    def select_student(self, student_id, student_name):
        self.student_id = student_id
        self.ids.search_box.text = student_name
        # Clear the RecycleView data
        self.ids.results_view.data = []
