from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.app import App
from kivy.metrics import dp
from kivymd.uix.button import MDRoundFlatButton
# from models.student_model import Student

Builder.load_file('views/admin_edit_subjects_view.kv')

class AdminEditSubjectsView(Screen):

    subject_id = None
    student_metadata = None
    def on_enter(self):
        self.ed_squared_app = App.get_running_app()
        self.user_obj = self.ed_squared_app.current_user_obj
        self.populate_subjects()

    def on_load(self, student_metadata):
        self.student_metadata = student_metadata

    def populate_subjects(self):
        self.ids.subjects_grid.clear_widgets()
        subjects = self.user_obj.list_student_subjects(self.student_metadata["student_id"])
        if subjects:
            for subject in subjects:
                self.add_subject_row(subject["ID"], subject["NAME"])

    def add_subject_row(self, subject_id, subject_name):
        subject_label = Label(text=subject_name, color=(1, 1, 1, 1), text_size=(self.width, None), halign='center', valign='middle', font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        delete_button = MDRoundFlatButton(text='Delete', md_bg_color=(0.6667, 0.4196, 0.7765, 1), line_color=(1,1,1,1), text_color=(1,1,1,1), size_hint_x=0.2, font_name='utils/font/GalanoGrotesqueAltMedium.ttf')
        delete_button.bind(on_release=lambda instance, name=subject_name: self.delete_subject(subject_id))

        subject_label.bind(size=lambda instance, value: setattr(instance, 'text_size', (value[0], None)))

        self.ids.subjects_grid.add_widget(subject_label)
        self.ids.subjects_grid.add_widget(delete_button)

    def add_subject(self):
        print(f"Added for student: {self.student_metadata['student_id']} subject_id: {self.subject_id}")
        self.user_obj.update_subjects(self.student_metadata["student_id"], self.subject_id)
        self.populate_subjects()
        self.ids.search_box.text = ''

    def delete_subject(self, subject_id):
        self.user_obj.delete_student_subjects(self.student_metadata["student_id"], subject_id)
        print(f"Deleted for student: {self.student_metadata['student_id']} subject_id: {self.subject_id}")
        self.populate_subjects()
###
    def update_recycleview_height(self, search_result):
        # Increase the recycleview size if search result exists, else set it to 0
        if search_result:
            self.ids.results_view.height = dp(200)
        else:
            self.ids.results_view.height = 0

    def search_subject_keyword(self, keyword):
        # Retrieve and sanitize the keyword from searchbox, use an object to pass the keyword to the respective model
        self.ids.results_view.data = []
        self.update_recycleview_height(keyword)
        if keyword:
            keyword = keyword.strip().upper()
            response = self.user_obj.search_subjects_by_keyword(keyword)
            search_result = []
            # If response exists for the entered keyword, display them
            if response:
                for subject in response:
                    search_result.append((subject["ID"], subject["NAME"]))
                print(search_result)
                self.update_search_results(search_result)

    def update_search_results(self, search_result):
        # Updates recycleview content on every new query
        self.ids.results_view.data = [{'sub_id': sub_id, 'text': sub_name, 'on_select': self.select_subject} for sub_id, sub_name in search_result]

    def select_subject(self, subject_id, subject_name):
        # Set the id and name of the subject which is clicked from the recycleview
        self.subject_id = subject_id
        self.ids.search_box.text = subject_name
        self.ids.results_view.data = []
