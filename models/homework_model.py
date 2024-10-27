from .connection import connection_db

class Homework:
    def __init__(self, db_conn):
        self.db_conn = db_conn
    def admin_adds_hw(self, student_id, homework):
        current_row = self.view_homework(student_id, 1)
        if current_row:
            if current_row["STUDENT_ID"] == student_id and current_row["HOMEWORK"] != homework:
                query = """
                            INSERT INTO HOMEWORK (STUDENT_ID, HOMEWORK)
                            VALUES (%s, %s)
                        """
                params = (student_id, homework)
                executed = self.db_conn.execute_query(query, params)
                if executed:
                    print(f"Homework for student: {student_id} Added.")
                return True
        else:
            query = """
                        INSERT INTO HOMEWORK (STUDENT_ID, HOMEWORK)
                        VALUES (%s, %s)
                    """
            params = (student_id, homework)
            executed = self.db_conn.execute_query(query, params)
            if executed:
                print(f"Homework for student: {student_id} Added.")
            return True
        return False

    def view_homework(self, student_id, limit=None):
        query = """SELECT * FROM HOMEWORK WHERE STUDENT_ID = %s ORDER BY CREATED_AT DESC"""
        params = (student_id,)
        if limit == 1:
            row = self.db_conn.fetch_response(query, params, 1)
        else:
            row = self.db_conn.fetch_response(query, params, 0)
        if row:
            return row
        else:
            print(f"Error fetching homework for student: {student_id}")

    def update_homework_status(self, status, student_id, homework_id):
        query = """
                    UPDATE HOMEWORK
                    SET STATUS = %s
                    WHERE STUDENT_ID = %s AND ID = %s
                """
        params = (status, student_id, homework_id)
        executed = self.db_conn.execute_query(query, params)
        if executed:
            print(f"Homework Status for student: {student_id} Updated.")
            return True
        else:
            print(f"Homework Status for student: {student_id} Not Updated.")
            return False
