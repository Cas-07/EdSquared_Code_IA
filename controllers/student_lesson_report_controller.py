from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.metrics import dp
from kivy.app import App
from models.student_model import Student
from models.session_manager_model import SessionManager
import webbrowser

# Load the corresponding .kv file
Builder.load_file('views/student_lesson_report_view.kv')

class StudentLessonReportView(Screen):
    def load_lesson_reports(self, subject_id, subject_name):
        self.subject_id = subject_id
        self.subject_name = subject_name
        self.ed_squared_app = App.get_running_app()
        self.student_obj = self.ed_squared_app.current_user_obj
        self.ids.reports_grid.clear_widgets()
        self.ids.subject_label.text = self.subject_name
        self.set_lesson_reports()

    def set_lesson_reports(self):
        reports = self.student_obj.list_lesson_Reports(self.student_obj.id, self.subject_id)
        if reports:
            for report in reports:
                self.add_report_row(report["SUB_TOPIC"], report["LESSON_REPORT"], report["LESSON_LINK"], report["CREATED_AT"], report["HOMEWORK_SET"])

    def add_report_row(self, sub_topic, content, lesson_link, date, homework_var):
        report_date = Label(
            text=str(date.strftime('%d-%m-%Y')),
            font_size='20sp',
            color=(1, 1, 1, 1),
            halign='left',
            # valign='middle',
            font_name='utils/font/GalanoGrotesqueAltMedium.ttf',
            size_hint_y=None,  # Allow dynamic height
            size_hint_x=None,
            # text_size=(self.width, None)
        )
        report_date.bind(texture_size=lambda instance, value: setattr(instance, 'width', value[0]))
        report_date.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        report_subtopic = Label(
            text=sub_topic,
            font_size='20sp',
            color=(1, 1, 1, 1),
            halign='left',
            # valign='middle',
            font_name='utils/font/GalanoGrotesqueAltMedium.ttf',
            size_hint_y=None,
            size_hint_x=None,
            # text_size=(self.width, None)
        )
        report_subtopic.bind(texture_size=lambda instance, value: setattr(instance, 'width', value[0]))
        report_subtopic.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        report_content = Label(
            text=content,
            color=(1, 1, 1, 1),
            halign='justify',
            # valign='middle',
            font_name='utils/font/GalanoGrotesqueAltMedium.ttf',
            size_hint_y=None,
            size_hint_x=None,
            text_size=(Window.width*0.85, None)
        )
        report_content.bind(texture_size=lambda instance, value: setattr(instance, 'width', value[0]))
        report_content.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        if lesson_link:
            report_link = Label(
                text=f"[ref=website][color=#2e2eb3][u]{lesson_link}[/u][/color][/ref]",
                markup=True,
                color=(1, 1, 1, 1),
                halign='justify',
                # valign='middle',
                font_name='utils/font/GalanoGrotesqueAltMedium.ttf',
                size_hint_y=None,
                size_hint_x=None,
                text_size=(Window.width*0.85, None)
            )
            report_link.bind(on_ref_press=lambda instance, ref: self.on_link_click(instance, lesson_link))
            report_link.bind(texture_size=lambda instance, value: setattr(instance, 'width', value[0]))
            report_link.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        if homework_var:
            homework_set = "Homework is set."
            hs_color = (0, 1, 0, 1)
        else:
            homework_set = "Homework not set."
            hs_color = (1, 0, 0, 1)

        homework_label = Label(
            text=homework_set,
            halign='left',
            # valign='middle',
            color=hs_color,
            font_name='utils/font/GalanoGrotesqueAltMedium.ttf',
            size_hint_y=None,
            size_hint_x=None,
            # text_size=(self.width, None)
        )
        homework_label.bind(texture_size=lambda instance, value: setattr(instance, 'width', value[0]))
        homework_label.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))

        # # # Add a separator line after each report
        separator = Widget(size_hint_y=None, height=dp(5))
        # with separator.canvas:
        #     Color(1, 1, 1, 1)
        #     Rectangle(pos=separator.pos, size=(Window.width, dp(50)))
        # separator.bind(size=self.update_separator_rect)

        # Add labels to the grid
        self.ids.reports_grid.add_widget(report_date)
        self.ids.reports_grid.add_widget(report_subtopic)
        self.ids.reports_grid.add_widget(report_content)
        if lesson_link:
            self.ids.reports_grid.add_widget(report_link)
        self.ids.reports_grid.add_widget(homework_label)
        self.ids.reports_grid.add_widget(separator)

    def on_link_click(self, instance, value):
        webbrowser.open(value)
