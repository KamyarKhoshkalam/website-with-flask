from flask import Flask, render_template, request, send_from_directory, url_for, redirect,session
from database1 import users_Database
from werkzeug.utils import secure_filename
import os

from database2 import course_Database

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

user_info = {"name" : "","cart": []}
admin_info = {"name":"mehdi","password":"m1382"}

logged_in = False
admin_logged_in = False


@app.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        image_path = request.files.get("image")
        image_data = save_image(image_path)
        secQ = request.form.get("secQ")
        if not users_Database().get_user(username):
            users_Database().insert_data(username, email, password, image_data,secQ)
            global logged_in
            global user_info
            logged_in = True
            user_info["name"] = username
            return redirect(url_for('user',username=user_info['name']))
    return render_template("signup.html")

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        global logged_in
        global admin_logged_in
        global user_info
        username = request.form.get("username")
        password = request.form.get("password")
        user = users_Database().get_user(username)
        if admin_info["name"] == username and admin_info["password"] == password:
            admin_logged_in = True
            return redirect(url_for("home"))
        if user and user[3] == password:
            logged_in = True
            user_info["name"] = username
            return redirect(url_for("home"))
    return render_template("login.html")


@app.route("/login/forget",methods=["GET","POST"])
def forget_password():
    if request.method == "POST":
        global logged_in
        global admin_logged_in
        global user_info
        username = request.form.get("username")
        secQ = request.form.get("secQ")
        user = users_Database().get_user(username)
        if admin_info["name"] == username :
            admin_logged_in = True
            return redirect(url_for("home"))
        if user and user[6] == secQ:
            logged_in = True
            user_info["name"] = username
            return redirect(url_for("user_edit",username=username))
    return render_template("forget_password.html")



# home page 

@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "POST":
        serchinginput = request.form.get("searchcourse")
        if course_Database().get_info(serchinginput):
            return redirect(url_for("course_info", coursename = serchinginput))
    courses = course_Database().get_all_info()
    return render_template("home.html",logged_in=logged_in,admin_logged_in=admin_logged_in,courses=courses,user_info=user_info)



# admin panel

@app.route("/admin")
def admin():
    if admin_logged_in:
        return render_template("adminPanel.html")
    else:
        return redirect(url_for("home"))

@app.route("/admin/courses",methods=["POST","GET"])
def admin_courses():
    if admin_logged_in:
        if request.method == "POST":
            course_name = request.form.get("delete")
            course_Database().delete_courses(course_name)
        courses = course_Database().get_all_info()
        return render_template("admin_courses.html",courses=courses)
    else:
        return redirect(url_for("home"))

@app.route("/admin/courses/add",methods=["GET","POST"])
def admin_courses_add():
    if admin_logged_in:
        if request.method == "POST":
            title = request.form.get("title")
            description = request.form.get("description")
            image =request.files.get("image")
            path = save_image(image)
            course_Database().insert_info(title.lower(),description,path)
            return redirect(url_for("admin_courses"))
        return render_template("admin_courses_add.html")
    else:
        return redirect(url_for("home"))

@app.route("/admin/courses/edit/<courseName>",methods=["GET","POST"])
def admin_courses_edit(courseName):
    if admin_logged_in:
        course_info = course_Database().get_info(courseName)
        if request.method == "POST":
            description = request.form.get("description")
            photo = request.files.get("image")
            photo_path = save_image(photo)
            course_Database().update_courses(course_info[1],description,photo_path)
            return redirect(url_for("admin_courses"))
        return render_template("admin_courses_edit.html",course_info=course_info)
    else:
        return redirect(url_for("home"))

@app.route("/admin/students")
def admin_students():
    if admin_logged_in:
        return render_template("admin_students.html")
    else:
        return redirect(url_for("home"))
    
# course side    

@app.route("/course/<coursename>",methods=["GET","POST"])
def course_info(coursename):
    course = course_Database().get_info(coursename)
    if course :
        global user_info
        if request.method == "POST":
            name = request.form.get("name")
            if name not in user_info["cart"]:
                user_info["cart"].append(name)
        return render_template("course.html",course = course,logged_in=logged_in)
    else:
        return redirect(url_for("home"))


# user panel

@app.route("/user/<username>",methods=["POST","GET"])
def user(username):
    global user_info
    if logged_in and username == user_info["name"]:
        
        if request.method == "POST":
            name = request.form.get("name")
            user_info["cart"].remove(name)
        user = users_Database().get_user(username)
        user_courses = []
        if user[5]:
            for user_course in users_Database().select_courses(username):
                user_courses.append(course_Database().get_info(user_course))
        cart = []
        for item in user_info["cart"]:
            cart.append(course_Database().get_info(item))
        return render_template("userPanel.html",user=user,user_info=user_info,user_courses=user_courses,cart=cart)
    else :
        return redirect(url_for("home"))
    
@app.route("/user/<username>/edit",methods=["GET","POST"])
def user_edit(username):
    global user_info
    if logged_in and username == user_info["name"]:
        user = users_Database().get_user(username)
        if request.method =="POST":
            password = request.form.get("password")
            photo = request.files.get("image")
            photo_path = save_image(photo)
            email = request.form.get("email")
            users_Database().update_user(user[1],email,password,photo_path)
            return redirect(url_for("user",username = username))
        return render_template("userPanel_edit.html",user=user)
    else :
        return redirect(url_for("home"))

@app.route("/user/<username>/save2db")
def user_save(username):
    global user_info
    if logged_in and username == user_info["name"]:
        for item in user_info["cart"]:
            users_Database().add_course(username,item)
        user_info["cart"] = []
        return redirect(url_for("user",username=username))
    else :
        return redirect(url_for("home"))

@app.route('/logout')
def logout():
    global user_info
    global logged_in
    user_info = {"name": "", "cart": []}
    logged_in = False
    return redirect(url_for('home'))





# extra functions


@app.template_filter('basename')
def basename_filter(path):
    import os
    return os.path.basename(path)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('uploads', filename)

def save_image(file):
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    return file_path


# app run

if __name__ == '__main__':
    app.run(debug=True)
