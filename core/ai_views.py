import os
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from google import genai
from .decorators import role_required
from .models import Enrollment, Student


def _get_genai_client():
  api_key = getattr(settings, 'GEMINI_API_KEY', None) or os.getenv(
      'GEMINI_API_KEY'
  )
  if not api_key:
    return None
  return genai.Client(api_key=api_key)


# =========================================================
# ENDPOINT 1: Per-Student Summary (Admin Only, POST, Saved to DB)
# =========================================================
@role_required('Admin')
@require_POST
def generate_student_summary(request, student_id):
  student = get_object_or_404(Student, id=student_id)
  client = _get_genai_client()

  if not client:
    messages.error(
        request, 'Gemini is not configured. Please set GEMINI_API_KEY in .env.'
    )
    return redirect('student-detail', student_id=student.id)

  enrollments = Enrollment.objects.filter(student=student).select_related(
      'course'
  )
  course_data = []

  for e in enrollments:
    try:
      result = e.result
      marks = result.marks
      remarks = result.remarks if result.remarks else 'No remarks'
    except ObjectDoesNotExist:
      marks = 'Pending / Not Graded'
      remarks = 'No remarks'

    course_data.append(
        f'Course: {e.course.title}, Marks: {marks}, Remarks: {remarks}'
    )

  courses_text = (
      '\n'.join(course_data) if course_data else 'No courses enrolled.'
  )

  prompt = (
      'You are an academic advisor. Given the following student profile and'
      ' course performance data, write a concise professional performance'
      ' summary of 3–5 sentences.\n\n'
      f'Student Name: {student.name}\n'
      f'Age: {student.age}\n'
      f'Courses Performance:\n{courses_text}'
  )

  try:
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
    )
    student.ai_summary = response.text
    student.save()
    messages.success(
        request, 'AI performance summary generated and saved successfully.'
    )
  except Exception as e:
    messages.error(request, f'Failed to generate summary: {e}')

  return redirect('student-detail', student_id=student.id)


# =========================================================
# ENDPOINT 2: Full Enrollment Report (Admin Only, POST, NOT stored in DB)
# =========================================================
@role_required('Admin')
@require_POST
def generate_enrollment_report(request):
  client = _get_genai_client()

  if not client:
    messages.error(
        request, 'Gemini is not configured. Please set GEMINI_API_KEY in .env.'
    )
    return redirect('admin-dashboard')

  all_enrollments = Enrollment.objects.select_related(
      'student', 'course'
  ).all()
  enrollment_records = []

  for e in all_enrollments:
    try:
      result = e.result
      marks = result.marks
      remarks = result.remarks if result.remarks else 'No remarks'
    except ObjectDoesNotExist:
      marks = 'Pending / Not Graded'
      remarks = 'No remarks logged'

    enrollment_records.append(
        f'Student: {e.student.name}, Course: {e.course.title}, Marks: {marks},'
        f' Remarks: {remarks}'
    )

  all_data_text = (
      '\n'.join(enrollment_records)
      if enrollment_records
      else 'No active student enrollments available.'
  )

  prompt = (
      'You are an academic administrator. Given the following comprehensive'
      ' institutional enrollment and student performance data, generate an'
      ' executive-level enrollment report. Summarize overall enrollment trends,'
      ' highlight outstanding student achievements, identify missing or'
      ' pending grades, and provide actionable recommendations for academic'
      ' departments.\n\n'
      f'Enrollment & Grading Records:\n{all_data_text}'
  )

  try:
    response = client.models.generate_content(
        model='gemini-3.6-flash',
        contents=prompt,
    )

    # Render directly to the page without writing to database
    return render(
        request,
        'admin_dashboard/enrollment_report.html',
        {
            'report': response.text,
            'total_enrollments': len(all_enrollments),
        },
    )

  except Exception as e:
    messages.error(request, f'Failed to generate enrollment report: {e}')
    return redirect('admin-dashboard')