from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'
client = MongoClient('localhost', 27017)
db = client['FlaskStudent']
students_collection = db['flask']
users_collection = db['users']
admins_collection = db['admins']

try:
    client.admin.command('ping')
    if students_collection.count_documents({}) == 0:
        students_collection.insert_many([
            {'roll_no': 1, 'name': 'Alice', 'age': 20, 'department': 'Physics', 'approved': False},
            {'roll_no': 2, 'name': 'Bob', 'age': 21, 'department': 'Chemistry', 'approved': False},
            {'roll_no': 3, 'name': 'Charlie', 'age': 22, 'department': 'Mathematics', 'approved': False}
        ])
    if admins_collection.count_documents({}) == 0:
        admins_collection.insert_one({'username': 'admin', 'password': 'admin123'})
    if users_collection.count_documents({}) == 0:
        users_collection.insert_one({'username': 'user', 'password': 'user123'})
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
from flask import session
app.config['SESSION_TYPE'] = 'filesystem'


from flask import session
app.config['SESSION_TYPE'] = 'filesystem'


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if users_collection.find_one({'username': username}):
            flash('Username already exists!', 'danger')
        else:
            users_collection.insert_one({'username': username, 'password': password})
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']
        if role == 'admin':
            admin = admins_collection.find_one({'username': username, 'password': password})
            if admin:
                session['username'] = username
                session['role'] = 'admin'
                flash('Admin login successful!', 'success')
                return redirect(url_for('admin_dashboard'))
        else:
            user = users_collection.find_one({'username': username, 'password': password})
            if user:
                session['username'] = username
                session['role'] = 'user'
                flash('User login successful!', 'success')
                return redirect(url_for('user_dashboard'))
        flash('Invalid credentials!', 'danger')
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'info')
    return redirect(url_for('login'))

# Admin dashboard
@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    students = list(students_collection.find())
    return render_template('admin_dashboard.html', students=students)

@app.route('/user', methods=['GET', 'POST'])
def user_dashboard():
    if session.get('role') != 'user':
        return redirect(url_for('login'))
    username = session.get('username')
    student = students_collection.find_one({'name': username})
    approved_students = list(students_collection.find({'approved': True}))
    if request.method == 'POST':
        roll_no = int(request.form['roll_no'])
        name = request.form['name']
        age = int(request.form['age'])
        department = request.form['department']
        if students_collection.find_one({'roll_no': roll_no}):
            flash('Roll number already exists!', 'danger')
        else:
            students_collection.insert_one({
                'roll_no': roll_no,
                'name': name,
                'age': age,
                'department': department,
                'approved': False
            })
            flash('Your details have been submitted for approval!', 'success')
            student = students_collection.find_one({'name': name})
    return render_template('user_dashboard.html', student=student, approved_students=approved_students)

# Approve student (admin only)
@app.route('/approve/<int:roll_no>', methods=['POST'])
def approve_student(roll_no):
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    result = students_collection.update_one({'roll_no': roll_no}, {'$set': {'approved': True}})
    if result.matched_count:
        flash('Student approved!', 'success')
    else:
        flash('Student not found!', 'danger')
    return redirect(url_for('admin_dashboard'))

# Home route redirects to login if not authenticated
@app.route('/')
def index():
    if not session.get('username'):
        return redirect(url_for('login'))
    if session.get('role') == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif session.get('role') == 'user':
        return redirect(url_for('user_dashboard'))

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
