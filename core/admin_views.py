from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

from .models import Student, Course, Enrollment
from .decorators import role_required


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@role_required("Admin")
def admin_dashboard(request):

    students_list = Student.objects.all()

    query = request.GET.get(
        "q",
        ""
    ).strip()

    teacher_id = request.GET.get("teacher")

    teachers = User.objects.filter(
        groups__name="Teacher"
    ).distinct()

    if query:

        students_list = students_list.filter(
            name__icontains=query
        ) | students_list.filter(
            user__email__icontains=query
        )

    if teacher_id:

        student_ids = Enrollment.objects.filter(
            course__assigned_teacher_id=teacher_id
        ).values_list(
            "student_id",
            flat=True
        )

        students_list = students_list.filter(
            id__in=student_ids
        ).distinct()

    paginator = Paginator(
        students_list,
        5
    )

    page_number = request.GET.get("page")

    students = paginator.get_page(
        page_number
    )

    return render(
        request,
        "admin_dashboard/dashboard.html",
        {
            "students": students,
            "query": query,
            "teachers": teachers,
            "teacher_id": teacher_id
        }
    )


# =========================================================
# ADMIN - STUDENT DETAIL
# =========================================================

@role_required("Admin")
def student_detail(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    return render(
        request,
        "admin_dashboard/student_detail.html",
        {
            "student": student
        }
    )


# =========================================================
# ADMIN - EDIT STUDENT
# =========================================================

@role_required("Admin")
def student_edit(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "POST":

        student.name = request.POST.get("name")
        student.age = request.POST.get("age")

        student.user.email = request.POST.get("email")

        student.user.save()
        student.save()

        messages.success(
            request,
            "Student updated successfully."
        )

        return redirect(
            "student-detail",
            student_id=student.id
        )

    return render(
        request,
        "admin_dashboard/student_edit.html",
        {
            "student": student
        }
    )


# =========================================================
# ADMIN - DELETE STUDENT
# =========================================================

@role_required("Admin")
def student_delete(request, student_id):

    student = get_object_or_404(
        Student,
        id=student_id
    )

    if request.method == "POST":

        student.delete()

        messages.success(
            request,
            "Student deleted successfully."
        )

        return redirect(
            "admin-dashboard"
        )

    return render(
        request,
        "admin_dashboard/delete.html",
        {
            "student": student
        }
    )


# =========================================================
# ADMIN - COURSE LIST
# =========================================================

@role_required("Admin")
def course_list(request):

    courses = Course.objects.all()

    query = request.GET.get(
        "q",
        ""
    ).strip()

    teacher_id = request.GET.get("teacher")

    teachers = User.objects.filter(
        groups__name="Teacher"
    ).distinct()

    if query:

        courses = courses.filter(
            title__icontains=query
        )

    if teacher_id:

        courses = courses.filter(
            assigned_teacher_id=teacher_id
        )

    paginator = Paginator(
        courses,
        5
    )

    page_number = request.GET.get("page")

    courses = paginator.get_page(
        page_number
    )

    return render(
        request,
        "admin_dashboard/course.html",
        {
            "courses": courses,
            "query": query,
            "teachers": teachers,
            "teacher_id": teacher_id
        }
    )


# =========================================================
# ADMIN - CREATE COURSE
# =========================================================

@role_required("Admin")
def course_create(request):

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        duration = request.POST.get("duration")
        teacher_id = request.POST.get("teacher")

        teacher = get_object_or_404(
            User,
            id=teacher_id,
            groups__name="Teacher"
        )

        Course.objects.create(
            title=title,
            description=description,
            duration=duration,
            assigned_teacher=teacher
        )

        messages.success(
            request,
            "Course added successfully."
        )

        return redirect(
            "course-list"
        )

    teachers = User.objects.filter(
        groups__name="Teacher"
    ).distinct()

    return render(
        request,
        "admin_dashboard/course_create.html",
        {
            "teachers": teachers
        }
    )


# =========================================================
# ADMIN - EDIT COURSE
# =========================================================

@role_required("Admin")
def course_edit(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    if request.method == "POST":

        course.title = request.POST.get("title")
        course.description = request.POST.get("description")
        course.duration = request.POST.get("duration")

        teacher_id = request.POST.get("teacher")

        teacher = get_object_or_404(
            User,
            id=teacher_id,
            groups__name="Teacher"
        )

        course.assigned_teacher = teacher

        course.save()

        messages.success(
            request,
            "Course updated successfully."
        )

        return redirect(
            "course-list"
        )

    teachers = User.objects.filter(
        groups__name="Teacher"
    ).distinct()

    return render(
        request,
        "admin_dashboard/course_edit.html",
        {
            "teachers": teachers,
            "course": course
        }
    )


# =========================================================
# ADMIN - DELETE COURSE
# =========================================================

@role_required("Admin")
def course_delete(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id
    )

    if request.method == "POST":

        course.delete()

        messages.success(
            request,
            "Course deleted successfully."
        )

        return redirect(
            "course-list"
        )

    return render(
        request,
        "admin_dashboard/course_delete.html",
        {
            "course": course
        }
    )


# # =========================================================
# ADMIN - ENROLLMENT LIST
# =========================================================

@role_required("Admin")
def enrollment_list(request):

    enrollments = Enrollment.objects.select_related(
        "student",
        "student__user",
        "course",
        "course__assigned_teacher",
        "result"
    )

    query = request.GET.get("q", "").strip()
    course_id = request.GET.get("course")

    courses = Course.objects.all()

    if query:
        enrollments = enrollments.filter(
            student__name__icontains=query
        ) | enrollments.filter(
            course__title__icontains=query
        )

    if course_id:
        enrollments = enrollments.filter(
            course_id=course_id
        )

    paginator = Paginator(enrollments, 5)
    page_number = request.GET.get("page")
    enrollments_page = paginator.get_page(page_number)

    return render(
        request,
        "admin_dashboard/enrollment.html",
        {
            "enrollments": enrollments_page,
            "query": query,
            "courses": courses,
            "course_id": course_id,
        }
    )

# =========================================================
# ADMIN - CREATE ENROLLMENT
# =========================================================

@role_required("Admin")
def enrollment_create(request):

    if request.method == "POST":

        student_id = request.POST.get("student")
        course_id = request.POST.get("course")

        if Enrollment.objects.filter(
            student_id=student_id,
            course_id=course_id
        ).exists():

            messages.error(
                request,
                "This student is already enrolled in this course."
            )

            return redirect(
                "enrollment-create"
            )

        Enrollment.objects.create(
            student_id=student_id,
            course_id=course_id
        )

        messages.success(
            request,
            "Student enrolled successfully."
        )

        return redirect(
            "enrollment-list"
        )

    students = Student.objects.all()
    courses = Course.objects.all()

    return render(
        request,
        "admin_dashboard/enrollment_create.html",
        {
            "students": students,
            "courses": courses
        }
    )


# =========================================================
# ADMIN - EDIT ENROLLMENT
# =========================================================

@role_required("Admin")
def enrollment_edit(request, enrollment_id):

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id
    )

    if request.method == "POST":

        student_id = request.POST.get("student")
        course_id = request.POST.get("course")

        duplicate = Enrollment.objects.filter(
            student_id=student_id,
            course_id=course_id
        ).exclude(
            id=enrollment.id
        ).exists()

        if duplicate:

            messages.error(
                request,
                "This student is already enrolled in this course."
            )

            return redirect(
                "enrollment-edit",
                enrollment_id=enrollment.id
            )

        enrollment.student_id = student_id
        enrollment.course_id = course_id

        enrollment.save()

        messages.success(
            request,
            "Enrollment updated successfully."
        )

        return redirect(
            "enrollment-list"
        )

    students = Student.objects.all()
    courses = Course.objects.all()

    return render(
        request,
        "admin_dashboard/enrollment_edit.html",
        {
            "enrollment": enrollment,
            "students": students,
            "courses": courses
        }
    )


# =========================================================
# ADMIN - DELETE ENROLLMENT
# =========================================================

@role_required("Admin")
def enrollment_delete(request, enrollment_id):

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id
    )

    if request.method == "POST":

        enrollment.delete()

        messages.success(
            request,
            "Enrollment deleted successfully."
        )

        return redirect(
            "enrollment-list"
        )

    return render(
        request,
        "admin_dashboard/enrollment_delete.html",
        {
            "enrollment": enrollment
        }
    )


# =========================================================
# ADMIN - TEACHER LIST
# =========================================================

@role_required("Admin")
def teacher_list(request):

    teachers = User.objects.filter(
        groups__name="Teacher"
    ).distinct()

    paginator = Paginator(
        teachers,
        5
    )

    page_number = request.GET.get("page")

    teachers = paginator.get_page(
        page_number
    )

    return render(
        request,
        "admin_dashboard/teacher.html",
        {
            "teachers": teachers
        }
    )