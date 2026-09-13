# Student Management System

A full-stack Student Management System built with Django. The system provides separate dashboards and permissions for Admin, Teacher, and Student users.

## Features

### Admin
- Manage students
- View and manage teachers
- Create, edit and delete courses
- Manage student enrollments
- View and manage student results
- Search students by name or email
- Filter students by teacher
- Generate AI-based student performance summaries
- Generate AI-based enrollment reports

### Teacher
- View only assigned courses
- Create, edit and delete own courses
- View students enrolled in own courses
- Add and update student marks
- Add and update remarks
- Cannot access other teachers' courses

### Student
- View own profile
- View enrolled courses
- View teacher name
- View marks and remarks
- Cannot edit academic information
- Cannot access Admin or Teacher features

## Technologies Used

- Python
- Django
- SQLite
- HTML
- CSS
- Django Authentication
- Django Groups & Permissions
- Google Gemini API

## Project Structure

```text
student-management-system/
│
├── core/
├── static/
├── templates/
├── studetn_mange/
├── manage.py
├── requirements.txt
├── .gitignore
└── README.
## Installation

1. Create a virtual environment:
   python -m venv .venv

2. Activate it:
   .venv\Scripts\activate

3. Install requirements:
   pip install -r requirements.txt

4. Run migrations:
   python manage.py migrate

5. Seed sample data:
   python manage.py seed

6. Start the server:
   python manage.py runserver