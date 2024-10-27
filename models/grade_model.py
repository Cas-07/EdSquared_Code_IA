from models.connection import connection_db

class Grade:
    def __init__(self, db_conn):
        self.db_conn = db_conn
    def student_adds_grade(self, student_id, subject_id, exam_type, grade):
        query = """
                    INSERT INTO GRADES (STUDENT_ID, SUBJECT_ID, EXAM_TYPE, GRADE)
                    VALUES (%s, %s, %s, %s)
                """
        params = (student_id, subject_id, exam_type, grade)
        executed = self.db_conn.execute_query(query, params)
        if executed:
            print(f"Grade for student: {student_id} subject: {subject_id} Added.")
            return True
        else:
            print(f"Grade for student: {student_id} subject: {subject_id} Failed to Add.")
            return False

    def student_updates_grade(self, student_id, subject_id, exam_type, grade, curr_date):
        query = """
                    UPDATE GRADES SET
                    EXAM_TYPE = %s,
                    GRADE = %s
                    WHERE STUDENT_ID = %s AND SUBJECT_ID = %s AND DATE(ADDED_AT) = %s
                """
        params = (exam_type, grade, student_id, subject_id, curr_date)
        executed = self.db_conn.execute_query(query, params)
        if executed:
            print(f"Grade for student: {student_id} subject: {subject_id} Updated.")
            return True
        else:
            print(f"Grade for student: {student_id} subject: {subject_id} Failed to Update.")
            return False


    def view_grades_by_studentid(self, student_id, subject_id):
        query = """SELECT ADDED_AT, EXAM_TYPE, GRADE FROM GRADES WHERE STUDENT_ID = %s AND SUBJECT_ID = %s ORDER BY ADDED_AT DESC"""
        params = (student_id, subject_id)
        row = self.db_conn.fetch_response(query, params, 0)
        if row:
            return row
        else:
            print(f"Error fetching grades for student: {student_id} subject: {subject_id}")

    def get_last_5_grades(self, student_id, subject_id):
        query = """SELECT GRADE FROM GRADES
                    WHERE STUDENT_ID = %s AND SUBJECT_ID = %s ORDER BY ADDED_AT DESC
                    LIMIT 5
                """
        params = (student_id, subject_id)
        row = self.db_conn.fetch_response(query, params, 0)
        if row:
            return row
        else:
            print(f"Error fetching grades for Student: {student_id} Subject: {subject_id}")

    def list_same_day_grades(self, student_id, curr_date):
        query = """SELECT SUBJECT_ID FROM GRADES
                    WHERE STUDENT_ID = %s AND DATE(ADDED_AT) = %s
                """
        params = (student_id, curr_date)
        row = self.db_conn.fetch_response(query, params, 0)
        if row:
            return row
        else:
            print(f"Error fetching subject_ids for Student: {student_id} curr_date: {curr_date}")
