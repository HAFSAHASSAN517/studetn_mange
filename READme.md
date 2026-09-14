# Student Management System

A full-stack, role-based Student Management System built with Django. The application provides dedicated dashboards for Admin, Teacher, and Student users, with role-based access control, course management, student enrollment, result management, Django Admin integration, and Google Gemini AI features.

---

## 1. Project Overview

The Student Management System is a centralized academic management platform designed to manage students, teachers, courses, enrollments, and academic results.

The system uses Django's built-in authentication, groups, and permissions to implement Role-Based Access Control (RBAC).

Each user role has access only to the functionality and data relevant to that role.

The system also includes Google Gemini AI integration that allows administrators to generate:

- Individual student performance summaries
- Overall enrollment reports

The application uses Django templates for the frontend and SQLite as the database.

---

## 2. Main Features

### Authentication

- User registration
- User login
- User logout
- Password authentication using Django Auth
- Role selection during registration
- Automatic redirection based on user role
- Protected routes
- Unauthorized users receive a `403 Forbidden` response

### Role-Based Access Control

The system supports three main roles:

- Admin
- Teacher
- Student

Each role has different permissions and access levels.

### Student Management

Administrators can:

- View students
- Add students
- Edit student information
- Delete students
- Search students by name or email
- Filter students by teacher
- View individual student details
- Generate AI-based student summaries

### Teacher Management

Administrators can:

- View registered teachers
- View teacher information
- Manage teacher accounts through Django Admin

Teachers can:

- View their assigned courses
- Create courses
- Edit their own courses
- Delete their own courses
- View students enrolled in their courses
- Add and update student marks
- Add and update remarks

### Course Management

Administrators can:

- View all courses
- Add courses
- Edit courses
- Delete courses
- Search courses by title
- Filter courses by teacher

Teachers can:

- View their own courses
- Create courses
- Edit their own courses
- Delete their own courses

### Enrollment Management

Administrators can:

- View enrollments
- Create enrollments
- Edit enrollments
- Delete enrollments
- Search enrollments
- Filter enrollments by course
- View student and course information

The system prevents duplicate enrollment of the same student in the same course.

### Result Management

Teachers can:

- View students enrolled in their courses
- Add marks
- Update marks
- Add remarks
- Update remarks

Marks are restricted between `0` and `100`.

### Student Dashboard

Students can:

- View their own dashboard
- View their enrolled courses
- View assigned teachers
- View marks
- View remarks
- View their own profile
- View their AI-generated summary when available

Students cannot access other students' information.

### Django Admin

The project uses Django's built-in administration interface with Jazzmin styling.

Administrators can manage:

- Users
- Groups
- Permissions
- Students
- Teachers
- Courses
- Enrollments
- Results

### Search, Filtering and Pagination

The system includes:

- Search functionality
- Dropdown filtering
- Pagination
- Five records per page

Pagination is implemented for major listing pages.

### AI Integration

Administrators can generate AI-based reports using Google Gemini.

The system supports:

#### Student AI Summary

The AI summary uses information such as:

- Student name
- Age
- Enrolled courses
- Marks
- Remarks

The generated summary can be stored with the student's record.

#### Enrollment Report

The AI enrollment report provides a broader analysis of enrollment and academic data.

The enrollment report is generated dynamically and is not stored permanently.

---

# 3. User Roles

## Admin

The Admin has the highest level of access.

### Admin can:

- Access the Admin Dashboard
- Manage students
- Manage courses
- Manage enrollments
- View teachers
- Manage results
- Search and filter records
- Generate student AI summaries
- Generate enrollment AI reports
- Access Django Admin
- Manage Django groups and permissions

---

## Teacher

Teachers have access only to their own academic data.

### Teacher can:

- Access Teacher Dashboard
- View assigned courses
- Create courses
- Edit their own courses
- Delete their own courses
- View students enrolled in their courses
- Add student marks
- Update student marks
- Add remarks
- Update remarks

### Teacher restrictions:

- Cannot access another teacher's courses
- Cannot view students from another teacher's courses
- Cannot access Admin Dashboard
- Cannot generate Admin-only AI reports

---

## Student

Students have read-only access to their own academic information.

### Student can:

- Access Student Dashboard
- View their profile
- View enrolled courses
- View assigned teachers
- View marks
- View remarks
- View their AI summary

### Student restrictions:

- Cannot edit their academic information
- Cannot manage courses
- Cannot manage enrollments
- Cannot edit results
- Cannot access Admin Dashboard
- Cannot access Teacher Dashboard
- Cannot view other students' data

---

# 4. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Programming language |
| Django | Backend web framework |
| SQLite | Database |
| Django Auth | Authentication |
| Django Groups | Role management |
| Django Permissions | Access control |
| Django Templates | Frontend rendering |
| HTML5 | Page structure |
| CSS3 | Styling |
| Jazzmin | Django Admin interface styling |
| Google Gemini | AI-generated summaries and reports |

---

# 5. Database Models

The project contains four main application models.

## Student

The `Student` model stores student-specific information.

### Fields

- User
- Name
- Email
- Age
- Enrolled Date
- AI Summary

The Student model has a One-to-One relationship with Django's built-in `User` model.

---

## Course

The `Course` model stores academic course information.

### Fields

- Title
- Description
- Duration
- Assigned Teacher

Each course is assigned to a teacher.

---

## Enrollment

The `Enrollment` model connects students with courses.

### Fields

- Student
- Course
- Enrollment Date

A student cannot be enrolled in the same course more than once.

---

## Result

The `Result` model stores academic performance.

### Fields

- Enrollment
- Marks
- Remarks

Each enrollment can have one result.

Marks are restricted between `0` and `100`.

---

# 6. Database Relationships

The main relationships are:

```text
User
 │
 ├── Student
 │
 └── Teacher
        │
        └── Course
               │
               └── Enrollment
                      │
                      ├── Student
                      │
                      └── Result