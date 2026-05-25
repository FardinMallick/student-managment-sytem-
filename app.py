from flask import Flask, render_template, request, redirect
import mysql.connector

from dotenv import load_dotenv
import os

# =========================================
# LOAD ENVIRONMENT VARIABLES
# =========================================

load_dotenv()

# =========================================
# FLASK APP
# =========================================

app = Flask(__name__)

# =========================================
# MYSQL DATABASE CONNECTION
# =========================================

db = mysql.connector.connect(

    host=os.getenv("DB_HOST"),

    user=os.getenv("DB_USER"),

    password=os.getenv("DB_PASSWORD"),

    database=os.getenv("DB_NAME")

)

cursor = db.cursor()

# =========================================
# HOME PAGE
# =========================================

@app.route('/')
def home():

    cursor.execute(

        """

        SELECT * FROM students

        ORDER BY id DESC

        """

    )

    students = cursor.fetchall()

    return render_template(

        'index.html',

        students=students

    )

# =========================================
# ADD STUDENT
# =========================================

@app.route('/add', methods=['POST'])
def add_student():

    full_name = request.form['full_name']

    email = request.form['email']

    phone = request.form['phone']

    gender = request.form['gender']

    age = request.form['age']

    course = request.form['course']

    city = request.form['city']

    student_state = request.form['student_state']

    fees = request.form['fees']

    status = request.form['status']

    recommendation = request.form['recommendation']

    query = """

    INSERT INTO students

    (

        full_name,
        email,
        phone,
        gender,
        age,
        course,
        city,
        student_state,
        fees,
        status,
        recommendation

    )

    VALUES

    (

        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s,
        %s

    )

    """

    values = (

        full_name,
        email,
        phone,
        gender,
        age,
        course,
        city,
        student_state,
        fees,
        status,
        recommendation

    )

    cursor.execute(query, values)

    db.commit()

    return redirect('/')

# =========================================
# DELETE STUDENT
# =========================================

@app.route('/delete/<int:id>')
def delete_student(id):

    cursor.execute(

        """

        DELETE FROM students

        WHERE id=%s

        """,

        (id,)

    )

    db.commit()

    return redirect('/')

# =========================================
# EDIT PAGE
# =========================================

@app.route('/edit/<int:id>')
def edit_student(id):

    cursor.execute(

        """

        SELECT * FROM students

        WHERE id=%s

        """,

        (id,)

    )

    student = cursor.fetchone()

    return render_template(

        'edit.html',

        student=student

    )

# =========================================
# UPDATE STUDENT
# =========================================

@app.route('/update/<int:id>', methods=['POST'])
def update_student(id):

    full_name = request.form['full_name']

    email = request.form['email']

    phone = request.form['phone']

    gender = request.form['gender']

    age = request.form['age']

    course = request.form['course']

    city = request.form['city']

    student_state = request.form['student_state']

    fees = request.form['fees']

    status = request.form['status']

    recommendation = request.form['recommendation']

    query = """

    UPDATE students

    SET

        full_name=%s,
        email=%s,
        phone=%s,
        gender=%s,
        age=%s,
        course=%s,
        city=%s,
        student_state=%s,
        fees=%s,
        status=%s,
        recommendation=%s

    WHERE id=%s

    """

    values = (

        full_name,
        email,
        phone,
        gender,
        age,
        course,
        city,
        student_state,
        fees,
        status,
        recommendation,
        id

    )

    cursor.execute(query, values)

    db.commit()

    return redirect('/')

# =========================================
# TEST ROUTE
# =========================================

@app.route('/test')
def test():

    return "Flask Working Successfully 🔥"

# =========================================
# RUN FLASK SERVER
# =========================================

if __name__ == '__main__':

    app.run(

        host="0.0.0.0",

        port=5000,

        debug=True

    )