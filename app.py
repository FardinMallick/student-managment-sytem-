from flask import Flask, render_template, request, redirect
import sqlite3

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
# CREATE MAIN TABLE
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

# =========================================
# CREATE TRASH TABLE
# =========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS trash_students (

    id INTEGER PRIMARY KEY,

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

    return render_template('index.html')

# =========================================
# SHOW ALL STUDENTS
# =========================================

@app.route('/students')
def students():

    cursor.execute(
        "SELECT * FROM students ORDER BY id DESC"
    )

    all_students = cursor.fetchall()

    return render_template(
        'students.html',
        students=all_students
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

    return redirect('/students')

# =========================================
# DELETE STUDENT -> MOVE TO TRASH
# =========================================

@app.route('/delete/<int:id>')
def delete_student(id):

    cursor.execute(
        "SELECT * FROM students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    if student:

        cursor.execute("""

        INSERT INTO trash_students
        (
            id,
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
            ?,
            ?
        )

        """, student)

        cursor.execute(
            "DELETE FROM students WHERE id=?",
            (id,)
        )

        conn.commit()

    return redirect('/students')

# =========================================
# TRASH PAGE
# =========================================

@app.route('/trash')
def trash():

    cursor.execute(
        "SELECT * FROM trash_students ORDER BY id DESC"
    )

    deleted_students = cursor.fetchall()

    return render_template(
        'trash.html',
        students=deleted_students
    )

# =========================================
# RESTORE STUDENT
# =========================================

@app.route('/restore/<int:id>')
def restore_student(id):

    cursor.execute(
        "SELECT * FROM trash_students WHERE id=?",
        (id,)
    )

    student = cursor.fetchone()

    if student:

        cursor.execute("""

        INSERT INTO students
        (
            id,
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
            ?,
            ?
        )

        """, student)

        cursor.execute(
            "DELETE FROM trash_students WHERE id=?",
            (id,)
        )

        conn.commit()

    return redirect('/trash')

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

    return redirect('/students')

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
