from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Create your models here.
class Student(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=100)
  age = models.PositiveIntegerField()
  enrolled_on = models.DateField(auto_now_add=True)
  ai_summary = models.TextField(blank=True)

  def __str__(self):
    return self.name


class Course(models.Model):
  title = models.CharField(max_length=20)
  description = models.TextField()
  duration = models.CharField(max_length=30)
  assigned_teacher = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.title


class Enrollment(models.Model):
  student = models.ForeignKey(Student, on_delete=models.CASCADE)
  course = models.ForeignKey(Course, on_delete=models.CASCADE)
  enrollment_date = models.DateField(auto_now_add=True)

  class Meta:
    unique_together = ('student', 'course')

  def __str__(self):
    return f'{self.student}-{self.course}'

  @property
  def get_result(self):
    try:
      return self.result
    except Exception:
      return None


class Result(models.Model):
  enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE)
  marks = models.DecimalField(
      max_digits=5,
      decimal_places=2,
      validators=[
          MinValueValidator(Decimal('0.00')),
          MaxValueValidator(Decimal('100.00')),
      ],
  )
  remarks = models.TextField(blank=True)

  def __str__(self):
    return f'{self.enrollment} - {self.marks}'