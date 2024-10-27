from .connection import connection_db
from .subject_model import Subject
from .grade_model import Grade
from .homework_model import Homework
from .feedback_model import Feedback
from .user_model import User
from .lesson_report_model import LessonReport

import hashlib

class Student(User):
    """The Student class is a subclass/child class of the User class that encapsulates the behavior and attributes specific
    to a student. This class manages the interaction between the student user and the application's data, providing methods
    for student authentication, managing subjects, grades, and homework, as well as interacting with assigned tutors and
    reviewing feedback and lesson reports.

    Attributes:
        id (int): The unique identifier for the student user.
        email (str): The email address of the student user.
        first_name (str): The first name of the student user.
        last_name (str): The last name of the student user.
        db_conn (object): The database connection object for executing queries.
        subject_obj (Subject): An instance of the Subject class for managing student subjects.
        homework_obj (Homework): An instance of the Homework class for managing homework assignments.
        grade_obj (Grade): An instance of the Grade class for managing grades.
        feedback_obj (Feedback): An instance of the Feedback class for managing feedback.
        lesson_report_obj (LessonReport): An instance of the LessonReport class for managing lesson reports.

    Methods:
        get_student_details(student_email): Retrieves student details (first name, last name, password) based on the email provided.
        register_student(email, first_name, last_name, password, admin_code): Registers a new student and links them to an admin using a code.
        verify_admin_code(admin_code): Verifies the admin code provided during student registration.
        verify_password(password, stored_hash): Verifies if the provided password matches the stored hash.
        authenticate_student(email, password): Authenticates a student using their email and password.
        get_related_admins(student_id): Retrieves a list of admins related to the student.
        add_admin(student_id, admin_code): Links a student to an admin using the admin's code.
        remove_admin(student_id, admin_code): Removes the link between a student and an admin.
        search_subjects_by_keyword(keyword): Searches for subjects by a keyword.
        update_subjects(student_id, subject_id): Updates the subjects associated with the student.
        list_student_subjects(student_id): Lists all subjects associated with the student.
        delete_student_subjects(student_id, subject_id): Removes a subject associated with the student.
        fetch_grades_by_subject(student_id, subject_id): Retrieves the grades for a specific subject.
        upload_grades(student_id, subject_name, exam_type, grades): Uploads new grades for a specific subject.
        update_grades(student_id, subject_id, exam_type, grades, curr_date): Updates existing grades for a specific subject and exam type.
        fetch_subject_id(subject_name): Retrieves the ID of a subject based on its name.
        fetch_homework(student_id): Retrieves homework assigned to the student.
        update_homework_status(status, student_id, homework_id): Updates the status of a homework assignment.
        fetch_feedback_all_subjects(student_id): Retrieves feedback for all subjects associated with the student.
        check_grades_date(student_id, curr_date): Checks if there are any grades recorded on a specific date.
        list_lesson_Reports(student_id, subject_id): Lists all lesson reports for a specific subject."""

    def __init__(self, id=None, email=None):
        self.id = id
        self.email = email
        self.first_name = None
        self.last_name = None
        self.db_conn = connection_db()
        self.subject_obj = Subject(self.db_conn)
        self.homework_obj = Homework(self.db_conn)
        self.grade_obj = Grade(self.db_conn)
        self.feedback_obj = Feedback(self.db_conn)
        self.lesson_report_obj = LessonReport(self.db_conn)

    def get_student_details(self, student_email):
        query = """SELECT * FROM STUDENT WHERE EMAIL = %s"""
        params = (student_email,)
        row = self.db_conn.fetch_response(query, params, 1)
        if row:

            return row
        else:
            return False

    def update_password(self, student_id, new_password):
        query = """UPDATE STUDENT
                    SET PASSWORD = %s
                    WHERE ID = %s"""
        params = (new_password, student_id)
        executed = self.db_conn.execute_query(query, params)
        if executed:
            print(f"Password updated for student: {student_id}")
            return True

        print(f"Failed to update Password for student: {student_id}")
        return False

    def register_student(self, email, first_name, last_name, password, admin_code):
        admin_row = self.verify_admin_code(admin_code)

        if admin_row:
            admin_id = admin_row["ID"]
            admin_email = admin_row["EMAIL"]
            query = """
                        INSERT INTO STUDENT (EMAIL, FIRST_NAME, LAST_NAME, PASSWORD)
                        VALUES (%s, %s, %s, %s)
                    """
            params = (email, first_name, last_name, password)
            executed = self.db_conn.execute_query(query, params)
            if executed:
                retry = 3
                while (retry > 0):
                    query = """SELECT ID FROM STUDENT WHERE EMAIL = %s"""
                    params = (email,)
                    row = self.db_conn.fetch_response(query, params, 1)
                    if row:
                        student_id = row["ID"]
                        query = """
                                    INSERT INTO ADMIN_STUDENTS (ADMIN_ID, STUDENT_ID)
                                    VALUES (%s, %s)
                                """
                        params = (admin_id, student_id)
                        executed = self.db_conn.execute_query(query, params)
                        if executed:
                            return (True, admin_email)
                        else:
                            retry -=1
                    else:
                        retry -=1

                if retry == 0:
                    return False
            return False
        return False

    def verify_admin_code(self, admin_code):
        query = """
                    SELECT * FROM ADMIN WHERE CODE = %s
                """
        params = (admin_code,)
        row = self.db_conn.fetch_response(query, params, 1)
        if row:
            return row

        return False

    def verify_password(self, password, stored_hash):
        # Extract the salt from the stored hash
        salt = bytes.fromhex(stored_hash[:32])

        # Extract the original hashed password
        original_hashed_password = stored_hash[32:]

        # Hash the provided password with the extracted salt using SHA-256
        hash_obj = hashlib.sha256(salt + password.encode('utf-8'))
        hashed_password = hash_obj.hexdigest()

        # Compare the hashed password with the stored hash
        return hashed_password == original_hashed_password


    def authenticate_student(self, email, password):
        # Select query for retrieving student detail based on entered email, if exists
        query = """SELECT * FROM STUDENT WHERE EMAIL = %s"""
        params = (email,)
        row = self.db_conn.fetch_response(query, params, 1)
        if row: # If user exists, verify password and set the session variables and return the user object
            hashed_password = row["PASSWORD"]
            if self.verify_password(password, hashed_password):
                self.id = row["ID"]
                self.email = row["EMAIL"]
                self.first_name = row["FIRST_NAME"]
                self.last_name = row["LAST_NAME"]
                return self
        else:
            return False

    def get_related_admins(self, student_id):
        query = """SELECT ADMIN.FIRST_NAME, ADMIN.LAST_NAME, ADMIN.CODE
        FROM ADMIN JOIN ADMIN_STUDENTS ON ADMIN.ID = ADMIN_STUDENTS.ADMIN_ID
        WHERE ADMIN_STUDENTS.STUDENT_ID = %s"""
        params = (student_id,)
        row = self.db_conn.fetch_response(query, params, 0)
        if row:
            return row
        else:
            return False

    def add_admin(self, student_id, admin_code):
        query = """
                    INSERT INTO ADMIN_STUDENTS VALUES((SELECT ID FROM ADMIN WHERE CODE = %s), %s)
                """
        params = (admin_code, student_id)
        executed = self.db_conn.execute_query(query, params)
        if executed:
            return True
        else:
            print(f"Error adding Tutor: {admin_code}")

    def remove_admin(self, student_id, admin_code):
        query = """
                    DELETE FROM ADMIN_STUDENTS
                    WHERE ADMIN_ID = (SELECT ID FROM ADMIN WHERE CODE = %s)
                    AND STUDENT_ID = %s
                """
        params = (admin_code, student_id)
        executed = self.db_conn.execute_query(query, params)
        if executed:
            return True
        else:
            print(f"Error Removing Tutor: {admin_code}")

    def search_subjects_by_keyword(self, keyword):
        # Respective user object calls the required method from subject model
        return self.subject_obj.query_by_keyword(keyword)

    def update_subjects(self, student_id, subject_id):
        self.subject_obj.student_adds(student_id, subject_id)

    def list_student_subjects(self, student_id):
        return self.subject_obj.query_by_studentid(student_id)

    def delete_student_subjects(self, student_id, subject_id):
        return self.subject_obj.delete_by_studentid(student_id, subject_id)

    def fetch_grades_by_subject(self, student_id, subject_id):
        return self.grade_obj.view_grades_by_studentid(student_id, subject_id)

    def upload_grades(self, student_id, subject_name, exam_type, grades):
        subject_id = self.fetch_subject_id(subject_name)
        self.grade_obj.student_adds_grade(student_id, subject_id["ID"], exam_type, grades)

    def update_grades(self, student_id, subject_id, exam_type, grades, curr_date):
        self.grade_obj.student_updates_grade(student_id, subject_id, exam_type, grades, curr_date)

    def fetch_subject_id(self, subject_name):
        return self.subject_obj.get_subjectid_by_name(subject_name)

    def fetch_homework(self, student_id):
        return self.homework_obj.view_homework(student_id)

    def update_homework_status(self, status, student_id, homework_id):
        self.homework_obj.update_homework_status(status, student_id, homework_id)

    def fetch_feedback_all_subjects(self, student_id):
        return self.feedback_obj.view_feedback(student_id)

    def check_grades_date(self, student_id, curr_date):
        return self.grade_obj.list_same_day_grades(student_id, curr_date)

    def list_lesson_Reports(self, student_id, subject_id):
        return self.lesson_report_obj.fetch_report_by_studentid(student_id, subject_id)

# from cryptography.fernet import Fernet
#
# key = Fernet.generate_key()
# cipher_suite = Fernet(key)
# encrypted_password = cipher_suite.encrypt(password.encode())
