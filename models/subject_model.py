from .connection import connection_db

class Subject:
    def __init__(self, db_conn):
        self.db_conn = db_conn
    def student_adds(self, student_id, subject_id):
        query = """
                    INSERT INTO STUDENT_SUBJECTS (STUDENT_ID, SUBJECT_ID)
                    VALUES (%s, %s)
                """
        params = (student_id, subject_id)
        executed = self.db_conn.execute_query(query, params)
        if executed:
            print(f"Subject {subject_id} Added for Student: {student_id}.")

    def query_by_studentid(self, student_id):
        query = """SELECT SUB.ID, SUB.NAME FROM STUDENT_SUBJECTS SS
                    JOIN SUBJECTS SUB ON SUB.ID = SS.SUBJECT_ID
                    WHERE SS.STUDENT_ID = %s
                """
        params = (student_id,)
        row = self.db_conn.fetch_response(query, params, 0)
        if row:
            return row
        else:
            print(f"Error fetching subjects for student: {student_id}")

    def query_by_keyword(self, keyword):
        # Searches for all the subjects which start with the passed keyword
        query = """SELECT * FROM SUBJECTS
                    WHERE NAME like %s
                """
        keyword = f"{keyword}%"
        params = (keyword,)
        row = self.db_conn.fetch_response(query, params, 0)
        print(row)
        if row:
            return row
        else:
            print(f"Error fetching subjects for keyword: {keyword}")

    def delete_by_studentid(self, student_id, subject_id):
        query = """DELETE FROM STUDENT_SUBJECTS
                    WHERE STUDENT_ID =  %s AND SUBJECT_ID = %s
                """
        params = (student_id, subject_id)
        executed = self.db_conn.execute_query(query, params)
        if executed:
            print(f"Subject {subject_id} Removed for Student: {student_id}.")

    def get_subjectid_by_name(self, subject_name):
        query = """SELECT ID FROM SUBJECTS
                    WHERE NAME = %s
                """
        params = (subject_name,)
        row = self.db_conn.fetch_response(query, params, 1)
        if row:
            return row
        else:
            print(f"Error fetching Subject ID for: {subject_name}")
