from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Student, Course, Enrollment, Result

# 1. Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "get_email", "age", "enrolled_on")
    search_fields = ("name", "user__email")
    list_filter = ("enrolled_on",)

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = "Email"

# 2. Course Admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("title", "assigned_teacher", "duration")
    search_fields = ("title",)
    list_filter = ("assigned_teacher",)

# 3. Enrollment Admin
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("student", "course", "enrollment_date")
    search_fields = ("student__name", "course__title")
    list_filter = ("course", "enrollment_date")

# 4. Result Admin
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ("enrollment", "marks")
    search_fields = ("enrollment__student__name",)
    list_filter = ("marks",)

# 5. User Admin (re-registered to match table specs)
admin.site.unregister(User)

@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "get_groups")
    search_fields = ("username", "email")
    list_filter = ("groups",)

    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = "Groups"