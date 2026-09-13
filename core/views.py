from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied

from .form import RegisterationForm
from .models import Student, Course, Enrollment, Result
from .decorators import role_required
from .gemini import generate_ai_text


# =========================
# AUTHENTICATION
# =========================

def register(request):
    if request.method == "POST":
        form = RegisterationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your account has been created successfully.")
            return redirect("login")
    else:
        form = RegisterationForm()

    return render(request, "registeration/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.groups.filter(name="Admin").exists():
                return redirect("admin-dashboard")
            elif user.groups.filter(name="Teacher").exists():
                return redirect("teacher-dashboard")
            elif user.groups.filter(name="Student").exists():
                return redirect("student-dashboard")
            else:
                messages.error(request, "Your account has no assigned role.")
                logout(request)
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, "auth/login.html")


def user_logout(request):
    logout(request)
    return redirect("login")


# ==================================================
# TEACHER DASHBOARD & COURSE MANAGEMENT
# ==================================================

@role_required("Teacher")
def teacher_dashboard(request):
    courses = Course.objects.filter(assigned_teacher=request.user)
    paginator = Paginator(courses, 5)
    page_number = request.GET.get("page")
    courses_page = paginator.get_page(page_number)

    return render(request, "teacher/dashboard.html", {"courses": courses_page})


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
        messages.success(request, "Course created successfully.")
        return redirect("teacher-dashboard")

    return render(request, "teacher/course_create.html")


@role_required("Teacher")
def teacher_course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.assigned_teacher != request.user:
        raise PermissionDenied

    if request.method == "POST":
        course.title = request.POST.get("title")
        course.description = request.POST.get("description")
        course.duration = request.POST.get("duration")
        course.save()
        messages.success(request, "Course updated successfully.")
        return redirect("teacher-dashboard")

    return render(request, "teacher/course_edit.html", {"course": course})


@role_required("Teacher")
def teacher_course_del(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.assigned_teacher != request.user:
        raise PermissionDenied

    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect("teacher-dashboard")

    return render(request, "teacher/course_delete.html", {"course": course})


@role_required("Teacher")
def teacher_course_student(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if course.assigned_teacher != request.user:
        raise PermissionDenied

    enrollments = Enrollment.objects.filter(course=course).select_related("student", "student__user")
    return render(request, "teacher/course_students.html", {"course": course, "enrollments": enrollments})


@role_required("Teacher")
def teacher_result_edit(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    if enrollment.course.assigned_teacher != request.user:
        raise PermissionDenied

    result = Result.objects.filter(enrollment=enrollment).first()

    if request.method == "POST":
        marks_input = request.POST.get("marks")
        remarks_input = request.POST.get("remarks")

        try:
            marks_val = float(marks_input)
            if marks_val < 0 or marks_val > 100:
                messages.error(request, "Marks must be between 0 and 100.")
                return render(request, "teacher/result_edit.html", {"enrollment": enrollment, "result": result})
        except (ValueError, TypeError):
            messages.error(request, "Please enter a valid numeric value for marks.")
            return render(request, "teacher/result_edit.html", {"enrollment": enrollment, "result": result})

        if result is None:
            result = Result(enrollment=enrollment)

        result.marks = marks_val
        result.remarks = remarks_input
        result.save()

        messages.success(request, "Student result updated successfully.")
        return redirect("teacher-course-students", course_id=enrollment.course.id)

    return render(request, "teacher/result_edit.html", {"enrollment": enrollment, "result": result})


# ==================================================
# ADMIN DASHBOARD
# ==================================================
@role_required("Admin")
def admin_dashboard(request):
    students_list = Student.objects.all().select_related("user")

    query = request.GET.get("q", "").strip()
    teacher_id = request.GET.get("teacher")

    teachers = User.objects.filter(groups__name="Teacher").distinct()

    if query:
        students_list = students_list.filter(
            name__icontains=query
        ) | students_list.filter(
            user__email__icontains=query
        )

    # Sanitize teacher_id to ignore empty strings or literal "None"
    if teacher_id and teacher_id.strip() and teacher_id != "None":
        try:
            teacher_pk = int(teacher_id)
            student_ids = Enrollment.objects.filter(
                course__assigned_teacher_id=teacher_pk
            ).values_list("student_id", flat=True)
            students_list = students_list.filter(id__in=student_ids).distinct()
        except ValueError:
            teacher_id = ""
    else:
        teacher_id = ""

    paginator = Paginator(students_list, 5)
    page_number = request.GET.get("page")
    students = paginator.get_page(page_number)

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

# ==================================================
# STUDENT DASHBOARD
# ==================================================

@role_required("Student")
def student_dashboard(request):
    student = get_object_or_404(Student, user=request.user)

    enrollments_list = Enrollment.objects.filter(
        student=student
    ).select_related(
        "course",
        "course__assigned_teacher"
    )

    paginator = Paginator(enrollments_list, 5)
    page_number = request.GET.get("page")
    enrollments = paginator.get_page(page_number)

    return render(
        request,
        "student_dashboard/dashboard.html",
        {
            "student": student,
            "enrollments": enrollments
        }
    )


# ==================================================
# ADMIN - STUDENT MANAGEMENT & AI
# ==================================================

@role_required("Admin")
def student_detail(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, "admin_dashboard/student_detail.html", {"student": student})


@role_required("Admin")
def generate_student_summary(request, student_id):
    if request.method != "POST":
        raise PermissionDenied

    student = get_object_or_404(Student, id=student_id)
    enrollments = Enrollment.objects.filter(student=student).select_related("course", "course__assigned_teacher")

    performance = []
    for enrollment in enrollments:
        result = Result.objects.filter(enrollment=enrollment).first()
        marks_str = str(result.marks) if (result and result.marks is not None) else "Not recorded"
        remarks_str = result.remarks if (result and result.remarks) else "None"
        performance.append(
            f"Course: {enrollment.course.title}, Marks: {marks_str}, Remarks: {remarks_str}"
        )

    prompt = f"""
You are an academic advisor. Given the following student profile and course performance data, write a concise professional performance summary of 3–5 sentences.

Student Name: {student.name}
Age: {student.age}
Email: {student.user.email}

Course Performance:
{chr(10).join(performance)}
"""
    summary = generate_ai_text(prompt)
    student.ai_summary = summary
    student.save()

    messages.success(request, "AI summary generated successfully.")
    return redirect("student-detail", student_id=student.id)


@role_required("Admin")
def generate_enrollment_report(request):
    if request.method != "POST":
        raise PermissionDenied

    enrollments = Enrollment.objects.all().select_related("student", "course", "course__assigned_teacher")

    enrollment_data = []
    for enrollment in enrollments:
        result = Result.objects.filter(enrollment=enrollment).first()
        marks_str = str(result.marks) if (result and result.marks is not None) else "Not recorded"
        remarks_str = result.remarks if (result and result.remarks) else "None"
        enrollment_data.append(
            f"Student: {enrollment.student.name}, Course: {enrollment.course.title}, "
            f"Teacher: {enrollment.course.assigned_teacher.username}, Marks: {marks_str}, Remarks: {remarks_str}"
        )

    prompt = f"""
You are an academic administrator. Analyze the following enrollment
and academic performance data and write a concise professional report.
Identify overall performance patterns, strong areas, weak areas,
and any recommendations for improvement.

Enrollment Data:
{chr(10).join(enrollment_data)}
"""
    report = generate_ai_text(prompt)
    return render(request, "admin_dashboard/enrollment_report.html", {"report": report})


@role_required("Admin")
def student_edit(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        student.name = request.POST.get("name")
        student.age = request.POST.get("age")
        student.user.email = request.POST.get("email")
        student.user.save()
        student.save()

        messages.success(request, "Student updated successfully.")
        return redirect("student-detail", student_id=student.id)

    return render(request, "admin_dashboard/student_edit.html", {"student": student})


@role_required("Admin")
def student_delete(request, student_id):
    student = get_object_or_404(Student, id=student_id)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully.")
        return redirect("admin-dashboard")

    return render(request, "admin_dashboard/delete.html", {"student": student})


# ==================================================
# ADMIN - COURSE MANAGEMENT
# ==================================================

@role_required("Admin")
def course_list(request):
    courses = Course.objects.all()
    paginator = Paginator(courses, 5)
    page_number = request.GET.get("page")
    courses_page = paginator.get_page(page_number)

    return render(request, "admin_dashboard/course.html", {"courses": courses_page})


@role_required("Admin")
def course_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        duration = request.POST.get("duration")
        teacher_id = request.POST.get("teacher")

        Course.objects.create(
            title=title,
            description=description,
            duration=duration,
            assigned_teacher_id=teacher_id
        )
        messages.success(request, "Course added successfully.")
        return redirect("course-list")

    teachers = User.objects.filter(groups__name="Teacher")
    return render(request, "admin_dashboard/course_create.html", {"teachers": teachers})


@role_required("Admin")
def course_edit(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        course.title = request.POST.get("title")
        course.description = request.POST.get("description")
        course.duration = request.POST.get("duration")

        teacher_id = request.POST.get("teacher")
        get_object_or_404(User, id=teacher_id, groups__name="Teacher")
        course.assigned_teacher_id = teacher_id
        course.save()

        messages.success(request, "Course updated successfully.")
        return redirect("course-list")

    teachers = User.objects.filter(groups__name="Teacher")
    return render(request, "admin_dashboard/course_edit.html", {"teachers": teachers, "course": course})


@role_required("Admin")
def course_del(request, course_id):
    course = get_object_or_404(Course, id=course_id)

    if request.method == "POST":
        course.delete()
        messages.success(request, "Course deleted successfully.")
        return redirect("course-list")

    return render(request, "admin_dashboard/course_delete.html", {"course": course})


# ==================================================
# ADMIN - ENROLLMENT MANAGEMENT
# ==================================================

@role_required("Admin")
def enrollment_list(request):
    enrollments = Enrollment.objects.all().select_related("student", "course")
    paginator = Paginator(enrollments, 5)
    page_number = request.GET.get("page")
    enrollments_page = paginator.get_page(page_number)

    return render(request, "admin_dashboard/enrollment.html", {"enrollments": enrollments_page})


@role_required("Admin")
def enrollment_create(request):
    if request.method == "POST":
        student_id = request.POST.get("student")
        course_id = request.POST.get("course")

        if Enrollment.objects.filter(student_id=student_id, course_id=course_id).exists():
            messages.error(request, "This student is already enrolled in this course.")
            return redirect("enrollment-create")

        Enrollment.objects.create(student_id=student_id, course_id=course_id)
        messages.success(request, "Student enrolled successfully.")
        return redirect("enrollment-list")

    students = Student.objects.all()
    courses = Course.objects.all()
    return render(request, "admin_dashboard/enrollment_create.html", {"students": students, "courses": courses})


@role_required("Admin")
def enrollment_delete(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if request.method == "POST":
        enrollment.delete()
        messages.success(request, "Enrollment deleted successfully.")
        return redirect("enrollment-list")

    return render(request, "admin_dashboard/enrollment_delete.html", {"enrollment": enrollment})


@role_required("Admin")
def enrollment_edit(request, enrollment_id):
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if request.method == "POST":
        student_id = request.POST.get("student")
        course_id = request.POST.get("course")

        duplicate = Enrollment.objects.filter(
            student_id=student_id,
            course_id=course_id
        ).exclude(id=enrollment.id).exists()

        if duplicate:
            messages.error(request, "This student is already enrolled in this course.")
            return redirect("enrollment-edit", enrollment_id=enrollment.id)

        enrollment.student_id = student_id
        enrollment.course_id = course_id
        enrollment.save()

        messages.success(request, "Enrollment updated successfully.")
        return redirect("enrollment-list")

    students = Student.objects.all()
    courses = Course.objects.all()
    return render(
        request,
        "admin_dashboard/enrollment_edit.html",
        {"enrollment": enrollment, "students": students, "courses": courses}
    )


# ==================================================
# ADMIN - TEACHER MANAGEMENT
# ==================================================

@role_required("Admin")
def teacher_list(request):
    teachers = User.objects.filter(groups__name="Teacher").distinct()
    paginator = Paginator(teachers, 5)
    page_number = request.GET.get("page")
    teachers_page = paginator.get_page(page_number)

    return render(request, "admin_dashboard/teacher.html", {"teachers": teachers_page})