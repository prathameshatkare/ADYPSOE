from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # Use SQLite for simplicity
app.config['SECRET_KEY'] = 'your_secret_key'  # For flash messages
db = SQLAlchemy(app)

# Define the Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    roll_no = db.Column(db.String(20), nullable=False)
    course = db.Column(db.String(100), nullable=False)

# Function to get all students
def get_all_students():
    return Student.query.all()

@app.route('/')
def index():
    students = get_all_students()  # Get all students
    return render_template('index.html', students=students)

@app.route('/add_student', methods=['POST'])
def add_student():
    name = request.form['name']
    roll_no = request.form['roll_no']
    course = request.form['course']

    new_student = Student(name=name, roll_no=roll_no, course=course)
    db.session.add(new_student)
    db.session.commit()
    flash('Student added successfully!', 'success')
    return redirect('/')

@app.route('/delete_student/<int:id>', methods=['POST'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    flash('Student deleted successfully!', 'success')
    return redirect('/')

@app.route('/update_student/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.name = request.form['name']
        student.roll_no = request.form['roll_no']
        student.course = request.form['course']
        db.session.commit()
        flash('Student updated successfully!', 'success')
        return redirect('/')
    
    return render_template('update_student.html', student=student)

if __name__ == '__main__':
    with app.app_context():  # Wrap the create_all call in the application context
        db.create_all()  # Create the database tables
    app.run(debug=True)
