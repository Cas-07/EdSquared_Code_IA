from models.student_model import Student
from models.admin_model import Admin
import json
import os
from kivy.utils import platform

class SessionManager:
    """The SessionManager class is responsible for managing user sessions within the application. 
    It handles the login and logout processes, saves and loads session data to and from a .json file, 
    and ensures that session directories exist on the file system.

    Attributes:
        FILE_PATH (str): The file path where session data is stored, adjusted for different platforms.
        current_user_type (str or None): The type of the currently logged-in user (e.g., "Student", "Admin").
        current_user (User or None): The currently logged-in user object, which can be either a Student or Admin.

    Methods:
        login(user): Logs in a user and saves the session data.
        logout(): Logs out the current user and clears the session data
        get_current_user(): Returns the currently logged-in user object.
        get_current_user_type(): Returns the type of the currently logged-in user.
        save_session(loggedin): Saves the current session data to a JSON file.
        check_session_dir_exist(): Ensures that the directory for storing session data exists.
        load_session(): Loads session data from a JSON file, restoring the user session if it exists."""
    
    if platform == "ios":
        FILE_PATH = os.path.join(os.environ.get('HOME'), 'Documents', 'EdSquared_sessions', 'session.json')
    else:
        FILE_PATH = os.path.join('data', 'EdSquared_sessions', 'session.json')

    def __init__(self):
        self.current_user_type = None
        self.current_user = None
        self.load_session()

    def login(self, user):
        self.current_user = user
        self.save_session(True)

    def logout(self):
        self.current_user_type = None
        self.current_user = None
        self.save_session(False)

    def get_current_user(self):
        return self.current_user

    def get_current_user_type(self):
        return self.current_user_type

    def save_session(self, loggedin):
        # If user logs in, saves the session.json file with the respective details,
        # or if the user logs out, removes/delets the session.json file
        self.check_session_dir_exist()
        if loggedin:
            user_data = {"type": type(self.current_user).__name__, "data": self.current_user.to_dict()}
            with open(self.FILE_PATH, "w") as f:
                json.dump(user_data, f)
        else:
            if os.path.exists(self.FILE_PATH):
                os.remove(self.FILE_PATH)

    def check_session_dir_exist(self):
        # Ensure the directory exists before attempting to write
        directory = os.path.dirname(self.FILE_PATH)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def load_session(self):
        # When the application starts, checks for the session.json file, if present then
        # logs in the user with the stored details
        self.check_session_dir_exist()
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r") as f:
                user_data = json.load(f)
                user_type = user_data.get("type")
                user_info = user_data.get("data")
                if user_type == "Student":
                    self.current_user_type = user_type
                    self.current_user = Student.from_dict(user_info)
                elif user_type == "Admin":
                    self.current_user_type = user_type
                    self.current_user = Admin.from_dict(user_info)
        else:
            self.current_user_type = None
            self.current_user = None
