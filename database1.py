import pymysql
from database2 import course_Database

class users_Database:
    def __init__(self):
        self.db = pymysql.connect(
            host="127.0.0.1",
            user="root",
            database="users",
            password="your password"
        )
        self.cursor = self.db.cursor()

    def create_table(self):
        sql = (
            """
            CREATE TABLE customers (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), email VARCHAR(255), password VARCHAR(255), image_path VARCHAR(255), courses TEXT,secQ TEXT)
            """
        )
        self.cursor.execute(sql)

    def insert_data(self, username, email, password, image_path,secQ):
        sql = (
            """
            INSERT INTO customers (username, email, password, image_path,secQ) VALUES (%s, %s, %s, %s,%s)
            """
        )
        val = (username, email, password, image_path,secQ)
        self.cursor.execute(sql, val)
        self.db.commit()


    def get_user(self, username):
        sql = (
            """
            SELECT * FROM customers WHERE username = %s
            """
        )
        val = (username, )
        self.cursor.execute(sql, val)
        return self.cursor.fetchone()
    
    def get_all_users(self):
        sql = (
            """
            SELECT * FROM user
            """
        )
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    
    def update_user(self, username,email,password,image_path):
        sql = (
            """
            UPDATE customers 
            SET email = %s,
                image_path = %s,
                password = %s
            WHERE username = %s;
            """
        )
        val = (email,image_path,password,username)
        self.cursor.execute(sql, val)
        self.db.commit()
    
    def delete_user(self, title):
        sql = (
            """
            DELETE FROM customers WHERE username = %s
            """
        )
        val = (title, )
        self.cursor.execute(sql, val)
        self.db.commit()

    def select_courses(self,username):
        sql = "SELECT courses FROM customers WHERE username = %s"
        self.cursor.execute(sql, (username,))
        result = self.cursor.fetchone()
        if result:
            courses_str = result[0]
            if courses_str:
                courses_list = courses_str.split(',')
            else:
                courses_list = []
            return courses_list
        else:
            return result

    def add_course(self,username,course):
        user_course = self.select_courses(username)
        if course not in user_course:
            user_course.append(course)
            courses_str = ','.join(user_course)
            sql = "UPDATE customers SET courses = %s WHERE username = %s"
            values = (courses_str, username)
            self.cursor.execute(sql, values)
            self.db.commit()


    def remove_course(self,username,course):
        user_course = self.select_courses(username)
        if course in user_course:
            user_course.remove(course)
            courses_str = ','.join(user_course)
            sql = "UPDATE customers SET courses = %s WHERE username = %s"
            values = (courses_str, username)
            self.cursor.execute(sql, values)
            self.db.commit()

