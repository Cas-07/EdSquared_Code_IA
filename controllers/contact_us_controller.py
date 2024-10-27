from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.app import App
from models.admin_model import Admin
from kivymd.uix.button import MDRaisedButton
from models.session_manager_model import SessionManager
import webbrowser

# Load the corresponding .kv file
Builder.load_file('views/contact_us_view.kv')

class ContactUsView(Screen):
    def on_enter(self):
        print("contact us: contact.edsquared@gmail.com")
        print("help doc: https://github.com/Cas-07/EdSquared_documentation/blob/main/support.md")

    def open_email(self):
        email = 'mailto:contact.edsquared@gmail.com'
        webbrowser.open(email)

    def open_support_page(self):
        website = 'https://github.com/Cas-07/EdSquared_documentation/blob/main/support.md'
        webbrowser.open(website)
