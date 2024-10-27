from .connection import connection_db # Remove!!!!!

class Feedback:
    def __init__(self, db_conn):
        self.db_conn = db_conn
    def admin_adds_feedback(self, student_id, subject_id, feedback):
        # Query for adding feedback for a particular student and subject 
        query = """
                    INSERT INTO FEEDBACK (STUDENT_ID, SUBJECT_ID, FEEDBACK_TEXT)
                    VALUES (%s, %s, %s)
                """
        params = (student_id, subject_id, feedback)
        executed = self.db_conn.execute_query(query, params)
        if executed:
            print(f"Feedback for student: {student_id} subject: {subject_id} Added.")

    def view_feedback(self, student_id):
        # Query for fetching the most recent feedback for all the subjects for a student 
        query = """SELECT SUB.NAME, F.FEEDBACK_TEXT FROM FEEDBACK F
                    JOIN SUBJECTS SUB ON SUB.ID = F.SUBJECT_ID
                    JOIN STUDENT_SUBJECTS SS ON SS.SUBJECT_ID = SUB.ID
                    JOIN STUDENT STU ON SS.STUDENT_ID = STU.ID
                    WHERE STU.ID = %s AND F.CREATED_AT = (
                        SELECT MAX(F2.CREATED_AT)
                        FROM FEEDBACK F2
                        WHERE F2.SUBJECT_ID = F.SUBJECT_ID
                        AND F2.STUDENT_ID = STU.ID
                    )
                """
        params = (student_id,)
        row = self.db_conn.fetch_response(query, params, 0)
        if row:
            return row
        else:
            print(f"Error fetching feedback for student: {student_id}")

    def view_feedback_by_subject(self, student_id, subject_id):
        query = """SELECT FEEDBACK_TEXT FROM FEEDBACK
                    WHERE STUDENT_ID = %s AND SUBJECT_ID = %s
                    ORDER BY CREATED_AT DESC
                """
        params = (student_id, subject_id)
        row = self.db_conn.fetch_response(query, params, 1)
        if row:
            return row
        else:
            print(f"Error fetching feedback for student: {student_id} and subject: {subject_id}")
