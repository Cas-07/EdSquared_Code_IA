from .connection import connection_db
from .subject_model import Subject
from .user_model import User
from .homework_model import Homework
from .grade_model import Grade
from .feedback_model import Feedback
from .lesson_report_model import LessonReport
import hashlib

class Admin(User):
    """The Admin class is a subclass/child class of the User class that encapsulates the behavior and attributes specific
    to a tutor. This class manages the interaction between the admin user and the application's data, providing methods for
    admin authentication, managing students, assigning and reviewing homework, handling grades, providing feedback,
    and generating lesson reports.

    Attributes:
        id (int): The unique identifier for the admin user.
        email (str): The email address of the admin user.
        code (str): A specific code associated with the admin user for administrative operations.
        db_conn (object): The database connection object for executing queries.
        homework_obj (Homework): An instance of the Homework class for managing homework assignments.
        grade_obj (Grade): An instance of the Grade class for managing grades.
        feedback_obj (Feedback): An instance of the Feedback class for managing feedback.
        lesson_report_obj (LessonReport): An instance of the LessonReport class for managing lesson reports

    Methods:
        get_admin_details(admin_email): Retrieves admin details (first name, last name, password) based on the email provided.
        register_admin(first_name, last_name, mail, password, code): Registers a new admin in the database.
        verify_password(password, stored_hash): Verifies if the provided password matches the stored hash.
        authenticate_admin(email, password): Authenticates an admin using their email and password.
        get_code(): Retrieves the admin's code from the database.
        remove_student(admin_id, email): Removes a student associated with the admin from the database.
        fetch_students_summary(arg=None): Fetches a summary of students associated with the admin.
        search_student_by_keyword(admin_id, keyword): Searches for a student associated with the admin using a keyword.
        fetch_details_by_student_id(student_id): Fetches detailed information about a student by their ID.
        fetch_subject_grade_history(student_id, subject_id): Retrieves the grade history for a specific student and subject.
        assign_homework(student_id, homework_text): Assigns homework to a student
        fetch_homework(student_id, limit): Retrieves homework assigned to a student.
        fetch_last_5_grades(student_id, subject_id): Retrieves the last five grades for a specific student and subject.
        fetch_recent_feedback(student_id, subject_id): Retrieves recent feedback for a specific student and subject.
        save_student_feedback(student_id, subject_id, feedback_text): Saves feedback for a student and subject.
        save_lesson_report(student_id, subject_id, subtopic, report_content, date, homework_var): Saves a lesson report for a student.
        list_lesson_Reports(student_id, subject_id): Lists all lesson reports for a specific student and subject."""

    def __init__(self, id=None, email=None):
        self.id = id
        self.email = email
        self.code = None
        self.db_conn = connection_db()
        self.homework_obj = Homework(self.db_conn)
        self.grade_obj = Grade(self.db_conn)
        self.feedback_obj = Feedback(self.db_conn)
        self.lesson_report_obj = LessonReport(self.db_conn)
        self.subject_obj = Subject(self.db_conn)

    def get_admin_details(self, admin_email):
        query = """SELECT * FROM ADMIN WHERE EMAIL = %s"""
        params = (admin_email,)
        row = self.db_conn.fetch_response(query, params, 1)
        if row:
            return row

        return False

    def update_password(self, admin_id, new_password):
        query = """UPDATE ADMIN
                    SET PASSWORD = %s
                    WHERE ID = %s"""
        params = (new_password, admin_id)
        executed = self.db_conn.execute_query(query, params)
        if executed:
            print(f"Password updated for admin: {admin_id}")
            return True

        print(f"Failed to update Password for admin: {admin_id}")
        return False

    def register_admin(self, first_name, last_name, mail, password, code):
        query = """
                    INSERT INTO ADMIN (FIRST_NAME, LAST_NAME, EMAIL, PASSWORD, CODE)
                    VALUES (%s, %s, %s, %s, %s)
                """
        params = (first_name, last_name, mail, password, code)
        executed = self.db_conn.execute_query(query, params)
        if executed:
            return True

        return False

    def verify_password(self, password, stored_hash):
        salt = bytes.fromhex(stored_hash[:32])

        original_hashed_password = stored_hash[32:]

        hash_obj = hashlib.sha256(salt + password.encode('utf-8'))
        hashed_password = hash_obj.hexdigest()

        return hashed_password == original_hashed_password

    def authenticate_admin(self, email, password):
        query = """SELECT * FROM ADMIN WHERE EMAIL = %s"""
        params = (email,)
        row = self.db_conn.fetch_response(query, params, 1)
        if row:
            hashed_password = row["PASSWORD"]
            if self.verify_password(password, hashed_password):
                self.id = row["ID"]
                self.email = row["EMAIL"]
                self.code = row["CODE"]
                return self
        else:
            return False

    def get_code(self):
        query = """SELECT CODE FROM ADMIN WHERE EMAIL = %s"""
        params = (self.email,)
        row = self.db_conn.fetch_response(query, params, 1)
        if row:
            self.code = row['CODE']
            return self.code
        else:
            return False

    def remove_student(self, admin_id, email):
        query = """DELETE FROM ADMIN_STUDENTS WHERE STUDENT_ID = (SELECT ID FROM STUDENT WHERE EMAIL = %s) AND ADMIN_ID = %s"""
        params = (email, admin_id)
        executed = self.db_conn.execute_query(query, params)
        if executed:
            return True

        return False

    def fetch_students_summary(self, arg=None):
        if arg == 'LAST_NAME':
            query = """
                        SELECT ID, FIRST_NAME, LAST_NAME, EMAIL FROM STUDENT
                        JOIN ADMIN_STUDENTS ON STUDENT.ID = ADMIN_STUDENTS.STUDENT_ID
                        WHERE ADMIN_STUDENTS.ADMIN_ID = %s ORDER BY LAST_NAME;
                    """
        else:
            query = """
                        SELECT ID, FIRST_NAME, LAST_NAME, EMAIL FROM STUDENT
                        JOIN ADMIN_STUDENTS ON STUDENT.ID = ADMIN_STUDENTS.STUDENT_ID
                        WHERE ADMIN_STUDENTS.ADMIN_ID = %s;
                    """
        params = (self.id,)
        row = self.db_conn.fetch_response(query, params, 0)
        if row:
            return row

        return False

    def search_student_by_keyword(self, admin_id, keyword):
        query = """SELECT * FROM STUDENT
                    JOIN ADMIN_STUDENTS ON STUDENT.ID = ADMIN_STUDENTS.STUDENT_ID
                    WHERE ADMIN_STUDENTS.ADMIN_ID = %s
                    AND (STUDENT.FIRST_NAME like %s OR STUDENT.LAST_NAME Like %s)
                """
        keyword = f"{keyword}%"
        params = (admin_id, keyword, keyword)
        row = self.db_conn.fetch_response(query, params, 0)
        print(row)
        if row:
            return row
        else:
            print(f"Error fetching students for keyword: {keyword}")


    def fetch_details_by_student_id(self, student_id):
        query = """
                SELECT
                SUB.ID,
                SUB.NAME,
                SUB.COLOUR,
                COALESCE(G.EXAM_TYPE, 'N/A') AS EXAM_TYPE,
                COALESCE(G.GRADE, 'N/A') AS GRADE
            FROM
                SUBJECTS SUB
            LEFT JOIN
                GRADES G ON SUB.ID = G.SUBJECT_ID AND G.ADDED_AT = (
                    SELECT MAX(G2.ADDED_AT)
                    FROM GRADES G2
                    WHERE G2.SUBJECT_ID = SUB.ID
                    AND G2.STUDENT_ID = %s
                )
            JOIN
                STUDENT_SUBJECTS SS ON SS.SUBJECT_ID = SUB.ID
            JOIN
                STUDENT STU ON SS.STUDENT_ID = STU.ID
            WHERE
                STU.ID = %s;
                """
        params = (student_id, student_id)
        row = self.db_conn.fetch_response(query, params, 0)
        if row:
            return row

        return False

    def fetch_subject_grade_history(self, student_id, subject_id):
        query = """SELECT ADDED_AT, EXAM_TYPE, GRADE FROM GRADES
                    WHERE STUDENT_ID = %s AND SUBJECT_ID = %s ORDER BY ADDED_AT DESC
                """
        params = (student_id, subject_id)
        row = self.db_conn.fetch_response(query, params, 0)
        if row:
            return row

        return False

    def search_subjects_by_keyword(self, keyword):
        # Respective user object calls the required method from subject model
        return self.subject_obj.query_by_keyword(keyword)

    def update_subjects(self, student_id, subject_id):
        self.subject_obj.student_adds(student_id, subject_id)

    def list_student_subjects(self, student_id):
        return self.subject_obj.query_by_studentid(student_id)

    def delete_student_subjects(self, student_id, subject_id):
        return self.subject_obj.delete_by_studentid(student_id, subject_id)

    def check_grades_date(self, student_id, curr_date):
        return self.grade_obj.list_same_day_grades(student_id, curr_date)

    def upload_grades(self, student_id, subject_name, exam_type, grades):
        subject_id = self.fetch_subject_id(subject_name)
        self.grade_obj.student_adds_grade(student_id, subject_id["ID"], exam_type, grades)

    def update_grades(self, student_id, subject_id, exam_type, grades, curr_date):
        self.grade_obj.student_updates_grade(student_id, subject_id, exam_type, grades, curr_date)

    def fetch_subject_id(self, subject_name):
        return self.subject_obj.get_subjectid_by_name(subject_name)

    def assign_homework(self, student_id, homework_text):
        return self.homework_obj.admin_adds_hw(student_id, homework_text)

    def fetch_homework(self, student_id, limit):
        return self.homework_obj.view_homework(student_id, 1)

    def fetch_last_5_grades(self, student_id, subject_id):
        return self.grade_obj.get_last_5_grades(student_id, subject_id)

    def fetch_recent_feedback(self, student_id, subject_id):
        return self.feedback_obj.view_feedback_by_subject(student_id, subject_id)

    def save_student_feedback(self, student_id, subject_id, feedback_text):
        self.feedback_obj.admin_adds_feedback(student_id, subject_id, feedback_text)

    def save_lesson_report(self, student_id, subject_id, subtopic, report_content, lesson_link, date, homework_var):
        self.lesson_report_obj.upload_lesson_report(student_id, subject_id, subtopic, report_content, lesson_link, date, homework_var)

    def list_lesson_Reports(self, student_id, subject_id):
        return self.lesson_report_obj.fetch_report_by_studentid(student_id, subject_id)
