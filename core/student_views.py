from django.shortcuts import render, get_object_or_404

from .models import Student, Enrollment
from .decorators import role_required


# =========================================================
# STUDENT DASHBOARD
# =========================================================

@role_required("Student")
def student_dashboard(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    enrollments = Enrollment.objects.filter(
        student=student
    ).select_related(
        "course",
        "course__assigned_teacher"
    )

    return render(
        request,
        "student_dashboard/dashboard.html",
        {
            "student": student,
            "enrollments": enrollments
        }
    )


# =========================================================
# STUDENT PROFILE
# =========================================================

@role_required("Student")
def student_profile(request):

    student = get_object_or_404(
        Student,
        user=request.user
    )

    return render(
        request,
        "student_dashboard/profile.html",
        {
            "student": student
        }
    )