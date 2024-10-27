from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp
from models.student_model import Student

Builder.load_file('views/student_homework_view.kv')

class StudentHomeworkView(Screen):

    hw_status_lookup = dict()
    updated_status_lookup = dict()

    def on_enter(self):
        self.ed_squared_app = App.get_running_app()
        self.student_obj = self.ed_squared_app.current_user_obj
        self.ids.homework_grid.clear_widgets()
        self.student_homework()

    def student_homework(self):
        self.recent_homework = self.student_obj.fetch_homework(self.student_obj.id)
        if self.recent_homework:
            for homework in self.recent_homework:
                self.hw_status_lookup.update({homework['ID']: homework['STATUS']})
                self.add_homework_row(homework['ID'], homework['HOMEWORK'], homework['STATUS'])

    def add_homework_row(self, homework_id, homework_text, homework_status):
        homework_checkbox = MDCheckbox(active=homework_status, size_hint=(None, None), size=(dp(40), dp(40)), _md_bg_color=(1, 1, 1, 1))
        homework_checkbox.bind(active=lambda instance, value: self.update_homework_status(homework_id, instance.active, homework_status))

        homework_text = MDTextField(mode="fill", text=homework_text, multiline=True, readonly=True, background_color=(1, 1, 1, 1), foreground_color=(0, 0, 0, 1), size_hint_x=1, font_name='utils/font/GalanoGrotesqueAltMedium.ttf')

        self.ids.homework_grid.add_widget(homework_checkbox)
        self.ids.homework_grid.add_widget(homework_text)

    def update_homework_status(self, *args):
        if args[1] != args[2]:
            self.updated_status_lookup.update({args[0]: args[1]})
        else:
            if args[0] in self.updated_status_lookup:
                self.updated_status_lookup.pop(args[0])
        print('updated homework status', self.updated_status_lookup)

    def save_homework_status(self):
        for hw_id, hw_status in self.updated_status_lookup.items():
            homework_id = hw_id
            homework_status = hw_status
            if self.student_obj.update_homework_status(homework_status, self.student_obj.id, homework_id):
                print("Homework status updated.")
