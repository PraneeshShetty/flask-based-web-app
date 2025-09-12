from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'
client = MongoClient('localhost', 27017)
db = client['FlaskStudent']
students_collection = db['flask']

try:
    
    client.admin.command('ping')
    if students_collection.count_documents({}) == 0:
        students_collection.insert_many([
            {'roll_no': 1, 'name': 'Alice', 'age': 20, 'department': 'Physics'},
            {'roll_no': 2, 'name': 'Bob', 'age': 21, 'department': 'Chemistry'},
            {'roll_no': 3, 'name': 'Charlie', 'age': 22, 'department': 'Mathematics'}
        ])
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

@app.route('/')
def index():
    students = list(students_collection.find())
    return render_template('index.html', students=students)

# Add student
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        roll_no = int(request.form['roll_no'])
        name = request.form['name']
        age = int(request.form['age'])
        department = request.form['department']
        if students_collection.find_one({'roll_no': roll_no}):
            flash('Roll number already exists!', 'danger')
            return redirect(url_for('add_student'))
        students_collection.insert_one({
            'roll_no': roll_no,
            'name': name,
            'age': age,
            'department': department
        })
        flash('Student added successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('add.html')

# Delete student
@app.route('/delete/<int:roll_no>', methods=['POST'])
def delete_student(roll_no):
    result = students_collection.delete_one({'roll_no': roll_no})
    if result.deleted_count:
        flash('Student deleted successfully!', 'success')
    else:
        flash('Student not found!', 'danger')
    return redirect(url_for('index'))

@app.route('/update', methods=['GET', 'POST'])
def update_student():
    if request.method == 'POST':
        roll_no = int(request.form['roll_no'])
        name = request.form['name']
        age = int(request.form['age'])
        department = request.form['department']
        result = students_collection.update_one(
            {'roll_no': roll_no},
            {'$set': {'name': name, 'age': age, 'department': department}}
        )
        if result.matched_count:
            flash('Student details updated successfully!', 'success')
        else:
            flash('Student not found!', 'danger')
        return redirect(url_for('update_student'))
    else:
        roll_no = request.args.get('roll_no')
        student = None
        if roll_no:
            student = students_collection.find_one({'roll_no': int(roll_no)})
        return render_template('update.html', student=student)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
