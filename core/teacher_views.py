from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

from .models import Course, Enrollment, Result
from .decorators import role_required


# =========================================================
# TEACHER DASHBOARD
# =========================================================

@role_required("Teacher")
def teacher_dashboard(request):

    courses = Course.objects.filter(
        assigned_teacher=request.user
    )

    paginator = Paginator(courses, 5)

    page_number = request.GET.get("page")

    courses = paginator.get_page(page_number)

    return render(
        request,
        "teacher/dashboard.html",
        {
            "courses": courses
        }
    )


# =========================================================
# TEACHER - CREATE COURSE
# =========================================================

@role_required("Teacher")
def teacher_course_create(request):

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        duration = request.POST.get("duration")

        Course.objects.create(
            title=title,
            description=description,
            duration=duration,
            assigned_teacher=request.user
        )

        messages.success(
            request,
            "Course created successfully."
        )

        return redirect("teacher-dashboard")

    return render(
        request,
        "teacher/course_create.html"
    )


# =========================================================
# TEACHER - EDIT COURSE
# =========================================================

@role_required("Teacher")
def teacher_course_edit(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        assigned_teacher=request.user
    )

    if request.method == "POST":

        course.title = request.POST.get("title")
        course.description = request.POST.get("description")
        course.duration = request.POST.get("duration")

        course.save()

        messages.success(
            request,
            "Course updated successfully."
        )

        return redirect("teacher-dashboard")

    return render(
        request,
        "teacher/course_edit.html",
        {
            "course": course
        }
    )


# =========================================================
# TEACHER - DELETE COURSE
# =========================================================

@role_required("Teacher")
def teacher_course_delete(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        assigned_teacher=request.user
    )

    if request.method == "POST":

        course.delete()

        messages.success(
            request,
            "Course deleted successfully."
        )

        return redirect("teacher-dashboard")

    return render(
        request,
        "teacher/course_delete.html",
        {
            "course": course
        }
    )


# =========================================================
# TEACHER - VIEW ENROLLED STUDENTS
# =========================================================

@role_required("Teacher")
def teacher_course_students(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        assigned_teacher=request.user
    )

    enrollments = Enrollment.objects.filter(
        course=course
    ).select_related(
        "student",
        "student__user"
    )

    return render(
        request,
        "teacher/course_students.html",
        {
            "course": course,
            "enrollments": enrollments
        }
    )


# =========================================================
# TEACHER - CREATE / UPDATE RESULT
# =========================================================

@role_required("Teacher")
def teacher_result_edit(request, enrollment_id):

    enrollment = get_object_or_404(
        Enrollment,
        id=enrollment_id,
        course__assigned_teacher=request.user
    )

    result = Result.objects.filter(
        enrollment=enrollment
    ).first()

    if request.method == "POST":

        marks = request.POST.get("marks")
        remarks = request.POST.get("remarks")

        if result is None:

            result = Result(
                enrollment=enrollment
            )

        result.marks = marks
        result.remarks = remarks

        if result.enrollment.course.assigned_teacher != request.user:
            raise PermissionDenied

        result.save()

        messages.success(
            request,
            "Student result updated successfully."
        )

        return redirect(
            "teacher-course-students",
            course_id=enrollment.course.id
        )

    return render(
        request,
        "teacher/result_edit.html",
        {
            "enrollment": enrollment,
            "result": result
        }
    )