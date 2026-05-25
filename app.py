from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# =========================
# MYSQL CONNECTION
# =========================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="fardin0102",   # apna mysql password
    database="studentdb"
)

cursor = db.cursor()

# =========================
# HOME PAGE
# =========================

@app.route('/')
def home():

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    return render_template('index.html', students=students)

# =========================
# ADD STUDENT
# =========================

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

    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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
    db.commit()

    return redirect('/')

# =========================
# DELETE STUDENT
# =========================

@app.route('/delete/<int:id>')
def delete_student(id):

    cursor.execute("DELETE FROM students WHERE id=%s", (id,))
    db.commit()

    return redirect('/')

# =========================
# UPDATE STUDENT PAGE
# =========================

@app.route('/edit/<int:id>')
def edit_student(id):

    cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
    student = cursor.fetchone()

    return render_template('edit.html', student=student)

# =========================
# UPDATE STUDENT
# =========================

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
        full_name=%s,
        email=%s,
        phone=%s,
        gender=%s,
        age=%s,
        course=%s,
        city=%s,
        student_state=%s,
        recommendation=%s,
        fees=%s,
        status=%s
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
        recommendation,
        fees,
        status,
        id
    )

    cursor.execute(query, values)
    db.commit()

    return redirect('/')

# =========================
# TEST ROUTE
# =========================

@app.route('/test')
def test():
    return "Flask Working 🔥"

# =========================
# RUN APP
# =========================

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)