"""
URL configuration for studetn_mange project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.shortcuts import redirect

from .views import (
    register,
    user_login,
    user_logout,
)

from .admin_views import (
    admin_dashboard,
    student_detail,
    student_edit,
    student_delete,
    course_list,
    course_create,
    course_edit,
    course_delete,
    enrollment_list,
    enrollment_create,
    enrollment_edit,
    enrollment_delete,
    teacher_list,
)

from .teacher_views import (
    teacher_dashboard,
    teacher_course_create,
    teacher_course_edit,
    teacher_course_delete,
    teacher_course_students,
    teacher_result_edit,
)

from .student_views import (
    student_dashboard,
    student_profile,
)

from .ai_views import (
    generate_student_summary,
    generate_enrollment_report,
)


urlpatterns = [  path("", lambda request: redirect("login")),

    # =====================================================
    # AUTHENTICATION
    # =====================================================

    path(
        "register/",
        register,
        name="register"
    ),

    path(
        "login/",
        user_login,
        name="login"
    ),

    path(
        "logout/",
        user_logout,
        name="logout"
    ),


    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    path(
        "admin-dashboard/",
        admin_dashboard,
        name="admin-dashboard"
    ),

    # Students
    path(
        "student-detail/<int:student_id>/",
        student_detail,
        name="student-detail"
    ),

    path(
        "student-edit/<int:student_id>/",
        student_edit,
        name="student-edit"
    ),

    path(
        "student-delete/<int:student_id>/",
        student_delete,
        name="student-delete"
    ),

    # Teachers
    path(
        "teacher-list/",
        teacher_list,
        name="teacher-list"
    ),

    # Courses
    path(
        "course-list/",
        course_list,
        name="course-list"
    ),

    path(
        "course-create/",
        course_create,
        name="course-create"
    ),

    path(
        "course-edit/<int:course_id>/",
        course_edit,
        name="course-edit"
    ),

    path(
        "course-delete/<int:course_id>/",
        course_delete,
        name="course-delete"
    ),

    # Enrollments
    path(
        "enrollment/",
        enrollment_list,
        name="enrollment-list"
    ),

    path(
        "enrollment-create/",
        enrollment_create,
        name="enrollment-create"
    ),

    path(
        "enrollment-edit/<int:enrollment_id>/",
        enrollment_edit,
        name="enrollment-edit"
    ),

    path(
        "enrollment-delete/<int:enrollment_id>/",
        enrollment_delete,
        name="enrollment-delete"
    ),


    # =====================================================
    # TEACHER
    # =====================================================

    path(
        "teacher-dashboard/",
        teacher_dashboard,
        name="teacher-dashboard"
    ),

    path(
        "teacher/courses/",
        teacher_dashboard,
        name="teacher-courses"
    ),

    path(
        "teacher/course-create/",
        teacher_course_create,
        name="teacher-course-create"
    ),

    path(
        "teacher/course-edit/<int:course_id>/",
        teacher_course_edit,
        name="teacher-course-edit"
    ),

    path(
        "teacher/course-delete/<int:course_id>/",
        teacher_course_delete,
        name="teacher-course-delete"
    ),

    path(
        "teacher/course-students/<int:course_id>/",
        teacher_course_students,
        name="teacher-course-students"
    ),

    path(
        "teacher/result-edit/<int:enrollment_id>/",
        teacher_result_edit,
        name="teacher-result-edit"
    ),


    # =====================================================
    # STUDENT
    # =====================================================

    path(
        "student-dashboard/",
        student_dashboard,
        name="student-dashboard"
    ),

    path(
        "student-profile/",
        student_profile,
        name="student-profile"
    ),


    # =====================================================
    # AI
    # =====================================================

    path(
        "students/<int:student_id>/generate-summary/",
        generate_student_summary,
        name="generate-student-summary"
    ),

    path(
        "generate-report/",
        generate_enrollment_report,
        name="generate-enrollment-report"
    ),
]