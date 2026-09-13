from decimal import Decimal
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Student, Course, Enrollment, Result


class Command(BaseCommand):
    help = "Seeds database with groups, permissions, users, courses, enrollments, and results."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting database seed...")

        # 1. Setup Groups and Django Model Permissions
        admin_group, _ = Group.objects.get_or_create(name="Admin")
        teacher_group, _ = Group.objects.get_or_create(name="Teacher")
        student_group, _ = Group.objects.get_or_create(name="Student")

        course_ct = ContentType.objects.get_for_model(Course)
        result_ct = ContentType.objects.get_for_model(Result)
        student_ct = ContentType.objects.get_for_model(Student)
        enrollment_ct = ContentType.objects.get_for_model(Enrollment)

        # Teacher model permissions
        teacher_perms = Permission.objects.filter(
            content_type__in=[course_ct, result_ct, student_ct, enrollment_ct],
            codename__in=[
                "view_course", "change_course", "add_course",
                "view_result", "add_result", "change_result",
                "view_student", "view_enrollment"
            ]
        )
        teacher_group.permissions.set(teacher_perms)

        # Admin model permissions
        admin_perms = Permission.objects.filter(
            content_type__in=[course_ct, result_ct, student_ct, enrollment_ct]
        )
        admin_group.permissions.set(admin_perms)

        # Student model permissions
        student_perms = Permission.objects.filter(
            content_type__in=[course_ct, enrollment_ct, result_ct],
            codename__in=["view_course", "view_enrollment", "view_result"]
        )
        student_group.permissions.set(student_perms)

        default_pwd = "Test@1234"

        # 2. Create Users
        # Admin
        admin_user, _ = User.objects.get_or_create(
            username="admin_user",
            email="admin@sms.com",
            defaults={"is_staff": True, "is_superuser": True}
        )
        admin_user.set_password(default_pwd)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()
        admin_user.groups.add(admin_group)

        # Teacher
        seed_teacher, _ = User.objects.get_or_create(
            username="teacher_user",
            email="teacher@sms.com",
            defaults={"is_staff": True}
        )
        seed_teacher.set_password(default_pwd)
        seed_teacher.is_staff = True
        seed_teacher.save()
        seed_teacher.groups.add(teacher_group)

        # Primary Student
        seed_student_user, _ = User.objects.get_or_create(
            username="student_user",
            email="student@sms.com"
        )
        seed_student_user.set_password(default_pwd)
        seed_student_user.save()
        seed_student_user.groups.add(student_group)

        seed_student, _ = Student.objects.get_or_create(
            user=seed_student_user,
            defaults={"name": "Primary Seed Student", "age": 20}
        )

        # 3. Create Dummy Students (At least 3)
        dummy_students = []
        for i in range(1, 4):
            u, _ = User.objects.get_or_create(
                username=f"dummy_student_{i}",
                email=f"dummy{i}@sms.com"
            )
            u.set_password(default_pwd)
            u.save()
            u.groups.add(student_group)

            s, _ = Student.objects.get_or_create(
                user=u,
                defaults={"name": f"Dummy Student {i}", "age": 19 + i}
            )
            dummy_students.append(s)

        # 4. Create 5 Courses assigned to Teacher
        courses = []
        course_data = [
            ("Python Basics", "Introduction to Python programming", "4 Weeks"),
            ("Django Web Dev", "Building scalable backends using Django", "6 Weeks"),
            ("Data Structures", "Core data structures and algorithms", "8 Weeks"),
            ("Database Systems", "Relational database modeling and SQL", "5 Weeks"),
            ("Applied AI/LLM", "Prompt engineering and API integrations", "4 Weeks"),
        ]

        for title, desc, duration in course_data:
            course, _ = Course.objects.get_or_create(
                title=title,
                defaults={
                    "description": desc,
                    "duration": duration,
                    "assigned_teacher": seed_teacher
                }
            )
            courses.append(course)

        # 5. Enrollments (Total: 15)
        seed_enrollments = []
        for course in courses:
            enr, _ = Enrollment.objects.get_or_create(
                student=seed_student,
                course=course
            )
            seed_enrollments.append(enr)

        dummy_enrollment_configs = [
            (dummy_students[0], courses[0]),
            (dummy_students[0], courses[1]),
            (dummy_students[0], courses[2]),
            (dummy_students[0], courses[3]),
            (dummy_students[1], courses[0]),
            (dummy_students[1], courses[1]),
            (dummy_students[1], courses[2]),
            (dummy_students[2], courses[2]),
            (dummy_students[2], courses[3]),
            (dummy_students[2], courses[4]),
        ]

        for student_obj, course_obj in dummy_enrollment_configs:
            Enrollment.objects.get_or_create(
                student=student_obj,
                course=course_obj
            )

        # 6. Results (5 graded results for primary student)
        sample_results = [
            (Decimal("92.50"), "Outstanding comprehension of fundamentals."),
            (Decimal("85.00"), "Good performance on backend architectures."),
            (Decimal("78.00"), "Solid problem-solving, work on optimization."),
            (Decimal("88.50"), "Demonstrated strong relational query skills."),
            (Decimal("95.00"), "Exceptional AI pipeline integration."),
        ]

        for enrollment, (marks, remarks) in zip(seed_enrollments, sample_results):
            Result.objects.update_or_create(
                enrollment=enrollment,
                defaults={"marks": marks, "remarks": remarks}
            )

        self.stdout.write(self.style.SUCCESS("Database seeded successfully with all required users, groups, permissions, and records!"))