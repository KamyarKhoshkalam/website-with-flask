import pymysql

class course_Database:
    def __init__(self):
        self.db = pymysql.connect(
            host="127.0.0.1",
            user="root",
            database="courses",
            password="your password"
        )
        self.cursor = self.db.cursor()

    def create_table_courses(self):
        sql = (
            """
            CREATE TABLE courseinfo (id INT AUTO_INCREMENT PRIMARY KEY, title VARCHAR(255), description MEDIUMTEXT, photo_path VARCHAR(255))
            """
        )
        self.cursor.execute(sql)

    def insert_info(self, title, description, photo_path):
        sql = (
            """
            INSERT INTO courseinfo (title, description, photo_path) VALUES (%s, %s, %s)
            """
        )
        val = (title, description, photo_path)
        self.cursor.execute(sql, val)
        self.db.commit()

    def get_info(self, title):
        sql = (
            """
            SELECT * FROM courseinfo WHERE title = %s
            """
        )
        val = (title, )
        self.cursor.execute(sql, val)
        return self.cursor.fetchone()
    
    def get_all_info(self):
        sql = (
            """
            SELECT * FROM courseinfo
            """
        )
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def delete_courses(self, title):
        sql = (
            """
            DELETE FROM courseinfo WHERE title = %s
            """
        )
        val = (title, )
        self.cursor.execute(sql, val)
        self.db.commit()

    def update_courses(self, title,description,photo_path):
        sql = (
            """
            UPDATE courseinfo 
            SET description = %s,
                photo_path= %s
            WHERE title = %s;
            """
        )
        val = (description,photo_path,title)
        self.cursor.execute(sql, val)
        self.db.commit()

