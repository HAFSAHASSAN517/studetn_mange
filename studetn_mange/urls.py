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
from django.contrib import admin
from django.urls import path
from core.views import register,user_login,user_logout
from core.views import teacher_dashboard,admin_dashboard,student_dashboard,student_detail,student_edit
from core.views import student_delete,course_list,course_create,course_edit,course_del
from core.views import teacher_course_create,teacher_course_edit,techer_course_del,teacher_course_student,teacher_result_edit
from core.views import enrollment_list,enrollment_create
from core.views import teacher_list,generate_student_summary,generate_enrollment_report
from core.views import enrollment_delete,enrollment_edit
urlpatterns = [
    path('admin/', admin.site.urls),
    path("register/",register,name="register"),
    path("login/",user_login,name="login"),
    path("teacher-dashboard/",teacher_dashboard,name="teacher-dashboard"),
    path("teacher/courses/", teacher_dashboard, name="teacher-courses"),
    path("logout/",user_logout,name="logout"),
    path("admin-dashboard/",admin_dashboard,name="admin-dashboard"),
    path("student-dashboard/",student_dashboard,name="student-dashboard"),
    path("student-detail/<int:student_id>/",student_detail,name="student-detail"),
    path("student-edit/<int:student_id>/",student_edit,name="student-edit"),
   path("student-delete/<int:student_id>/", student_delete, name="student-delete"),
    path("course-list/",course_list,name="course-list"),
    path("course-create/",course_create, name="course-create"),
    path("course-edit/<int:course_id>/",course_edit, name="course-edit"),
    path("course-del/<int:course_id>/",course_del,name="course-del"),
    path("teacher/course-create/",teacher_course_create,name="teacher-course-create"),
    
path(
    "teacher/course-edit/<int:course_id>/",
    teacher_course_edit,
    name="teacher-course-edit"
),
path("teacher/course-del/<int:course_id>/",techer_course_del,name="course-delete"),
path("teacher/course-student/<int:course_id>/",teacher_course_student,name="teacher-course-students"),
path("teacher/result-edit/<int:enrollment_id>/",teacher_result_edit,name="teacher-result-edit"),

path("enrollment-create/",enrollment_create,name="enrollment-create"),
path("teacher-list/",teacher_list,name="teacher-list"),
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
path("enrollment/", enrollment_list, name="enrollment-list"),
path(
    "enrollment-delete/<int:enrollment_id>/",
    enrollment_delete,
    name="enrollment-delete"
),
path(
    "enrollment-edit/<int:enrollment_id>/",
    enrollment_edit,
    name="enrollment-edit"
),





]
