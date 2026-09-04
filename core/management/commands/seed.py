from django.core.management.base import BaseCommand
from django.contrib.auth.models import User,Group
from core.models import Student,Course,Enrollment,Result
from decimal import Decimal
class Command(BaseCommand):
    help="seed the database with sample data"
    def handle(self,*args,**kwargs):
        self.stdout.write("seeding databse")
        admin_group,created= Group.objects.get_or_create(name="Admin")
        teacher_group,created = Group.objects.get_or_create(name="Teacher")
        student_group,created=Group.objects.get_or_create(name="Student")
        admin_user,created= User.objects.get_or_create(username="Admin")
        admin_user.email="admin@example.com"
        admin_user.set_password("Test@1234")
        admin_user.save()
        admin_user.groups.add(admin_group)
        teacher_user,created=User.objects.get_or_create(username="Teacher")
        teacher_user.email="teacher@example.com"
        teacher_user.set_password("Test@1234")
        teacher_user.save()
        teacher_user.groups.add(teacher_group)
        student_user,created=User.objects.get_or_create(username="Student")
        student_user.email="student@email.com"
        student_user.set_password("Test@1234")
        student_user.save()
        student_user.groups.add(student_group)   
        student,created=Student.objects.get_or_create(
            
            user=student_user,
            defaults={
                "name": "Test Student",
                "age": 20,
            }
        )                                         
        course1,created=Course.objects.get_or_create(
            title="Python",
            defaults={
                "description": "Python Programming Course",
                "duration": "3 Months",
                "assigned_teacher": teacher_user,
            }
        )
        course2,created=Course.objects.get_or_create(
            title="DSA"
            ,defaults={
                "description":"DSA COURSE",
                "duration": "3 months",
                "assigned_teacher":teacher_user,            }
        )
        enrollment,created= Enrollment.objects.get_or_create(
            student=student,
            course=course1,
        )
        Result.objects.get_or_create(
            enrollment=enrollment,
            defaults={
                 "marks":Decimal("85.00"),
            
                 "remarks":"Good Performance",
            }
        )
        self.stdout.write(
            self.style.SUCCESS("Database Seeded Successfully")
        )