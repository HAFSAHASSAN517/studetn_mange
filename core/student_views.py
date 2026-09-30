from django.shortcuts import get_object_or_404, render
from .decorators import role_required
from .models import Enrollment, Notice, Student


# =========================================================
# STUDENT DASHBOARD
# =========================================================


@role_required("Student")
def student_dashboard(request):
  student, created = Student.objects.get_or_create(
      user=request.user,
      defaults={
          "name": request.user.username,
          "age": 18,
      },
  )

  enrollments = Enrollment.objects.filter(student=student).select_related(
      "course", "course__assigned_teacher"
  )
  notices = Notice.objects.all()

  return render(
      request,
      "student_dashboard/dashboard.html",
      {
          "student": student,
          "enrollments": enrollments,
          "notices": notices,
      },
  )


# =========================================================
# STUDENT PROFILE
# =========================================================


@role_required("Student")
def student_profile(request):
  student = get_object_or_404(Student, user=request.user)

  return render(
      request, "student_dashboard/profile.html", {"student": student}
  )