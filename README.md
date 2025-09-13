# Flask Student Management Web App

A modern Flask-based web application for managing student records with user and admin authentication, approval workflow, and a MongoDB backend. The app features a dark-themed, attractive Bootstrap UI.

## Features

- **User Registration & Login**: Users can register and log in to submit their student details.
- **Admin Login**: Admins can log in to approve, update, or delete student records.
- **Student Approval Workflow**: Students added by users require admin approval before appearing in the approved list.
- **CRUD Operations**: Add, update, and delete student records.
- **Role-Based Dashboards**:
  - **Admin Dashboard**: View all students, approve or delete records.
  - **User Dashboard**: View all approved students and submit own details for approval.
- **Dark Theme UI**: Eye-catching, modern interface using Bootstrap and custom styles.

## Technologies Used

- **Flask** (Python web framework)
- **MongoDB** (NoSQL database, running on localhost)
- **Bootstrap** (Frontend styling)
- **HTML/CSS** (Custom templates)

## Getting Started

### Prerequisites

- Python 3.x
- MongoDB running locally (`localhost:27017`)
- Required Python packages:
  ```
  pip install flask pymongo
  ```

### Setup

1. **Clone the repository** (or copy the project files).
2. **Start MongoDB** on your machine.
3. **Run the Flask app**:
   ```
   python app.py
   ```
4. **Access the app** at [http://localhost:5000](http://localhost:5000).

### Default Credentials

- **Admin**
  - Username: `admin`
  - Password: `admin123`
- **User**
  - Username: `user`
  - Password: `user123`
- You can register new users via the registration page.

## Project Structure

```
e:\flask based web app\
│
├── app.py
├── templates\
│   ├── add.html
│   ├── admin_dashboard.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── update.html
│   └── user_dashboard.html
```

## Usage

- **Register** as a user and log in.
- **Submit your student details** (name, roll number, age, department).
- **Admin** logs in to approve or manage student records.
- **Approved students** are visible to all users.

## Customization

- Change admin credentials in `app.py` if needed.
- Update Bootstrap styles in HTML templates for further UI customization.

## License

This project is provided for educational purposes.

---

**Developed with Flask, MongoDB, and Bootstrap.**
