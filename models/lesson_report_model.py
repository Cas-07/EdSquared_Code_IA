from models.connection import connection_db

class LessonReport:
    def __init__(self, db_conn):
        self.db_conn = db_conn

    def fetch_report_by_studentid(self, student_id, subject_id):
        query = """SELECT SUB_TOPIC, LESSON_REPORT, LESSON_LINK, CREATED_AT, HOMEWORK_SET FROM LESSON_REPORT WHERE STUDENT_ID = %s AND SUBJECT_ID = %s ORDER BY CREATED_AT DESC"""
        params = (student_id, subject_id)
        row = self.db_conn.fetch_response(query, params, 0)
        if row:
            return row
        else:
            print(f"Error fetching lesson reports for student: {student_id} subject: {subject_id}")

    def upload_lesson_report(self, student_id, subject_id, subtopic, report_content, lesson_link, date, homework_var):
        query = """
                    INSERT INTO LESSON_REPORT (STUDENT_ID, SUBJECT_ID, SUB_TOPIC, LESSON_REPORT, LESSON_LINK, CREATED_AT, HOMEWORK_SET)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """
        params = (student_id, subject_id, subtopic, report_content, lesson_link, date, homework_var)
        executed = self.db_conn.execute_query(query, params)
        if executed:
            print(f"Lesson Report for student: {student_id} Added.")
