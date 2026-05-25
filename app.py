from flask import Flask, render_template, request, redirect
import sqlite3

# =========================================
# FLASK APP
# =========================================

app = Flask(__name__)

# =========================================
# SQLITE DATABASE CONNECTION
# =========================================

conn = sqlite3.connect(
    "students.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =========================================
# CREATE TABLE
# =========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS students (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_name TEXT,
    email TEXT,
    phone TEXT,
    gender TEXT,
    age TEXT,
    course TEXT,
    city TEXT,
    student_state TEXT,
    recommendation TEXT,
    fees TEXT,
    status TEXT

)

""")

conn.commit()

# =========================================
# HOME PAGE
# =========================================

@app.route('/')
def home():

    cursor.execute(
        "SELECT * FROM students ORDER BY id DESC"
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
    recommendation = request.form['recommendation']
    fees = request.form['fees']
    status = request.form['status']

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
        recommendation,
        fees,
        status
    )

    VALUES
    (
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?,
        ?
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
        recommendation,
        fees,
        status

    )

    cursor.execute(query, values)

    conn.commit()

    return redirect('/')

# =========================================
# DELETE STUDENT
# =========================================

@app.route('/delete/<int:id>')
def delete_student(id):

    cursor.execute(
        "DELETE FROM students WHERE id=?",
        (id,)
    )

    conn.commit()

    return redirect('/')

# =========================================
# EDIT PAGE
# =========================================

@app.route('/edit/<int:id>')
def edit_student(id):

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
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
    recommendation = request.form['recommendation']
    fees = request.form['fees']
    status = request.form['status']

    query = """

    UPDATE students

    SET

        full_name=?,
        email=?,
        phone=?,
        gender=?,
        age=?,
        course=?,
        city=?,
        student_state=?,
        recommendation=?,
        fees=?,
        status=?

    WHERE id=?

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
        recommendation,
        fees,
        status,
        id

    )

    cursor.execute(query, values)

    conn.commit()

    return redirect('/')

# =========================================
# TEST ROUTE
# =========================================

@app.route('/test')
def test():

    return "Student Management System Working Successfully 🔥"

# =========================================
# RUN SERVER
# =========================================

if __name__ == '__main__':

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )