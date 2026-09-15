from django.contrib import admin
from django.contrib.auth.models import User
from .models import Student, Enrollment, Course, Result

@admin.register(Student)
class AdminStudent(admin.ModelAdmin):
    list_display = ('name', 'student_email', 'age', 'enrolled_on')
    search_fields = ('name', 'user__email')
    list_filter = ('enrolled_on',)

    def student_email(self, obj):
        return obj.user.email

    student_email.short_description = 'Email'

@admin.register(Course)
class AdminCourse(admin.ModelAdmin):
    list_display = ('title', 'assigned_teacher', 'duration')
    search_fields = ('title',)
    list_filter = ('assigned_teacher',)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if request.user.groups.filter(name="Teacher").exists():
            return queryset.filter(assigned_teacher=request.user)

        return queryset

    def has_view_permission(self, request, obj=None):
        if obj is not None:
            if request.user.groups.filter(name="Teacher").exists():
                return obj.assigned_teacher == request.user

        return super().has_view_permission(request, obj)

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            if request.user.groups.filter(name="Teacher").exists():
                return obj.assigned_teacher == request.user

        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            if request.user.groups.filter(name="Teacher").exists():
                return obj.assigned_teacher == request.user

        return super().has_delete_permission(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if request.user.groups.filter(name="Teacher").exists():
            return ('assigned_teacher',)

        return ()

    def save_model(self, request, obj, form, change):
        if request.user.groups.filter(name="Teacher").exists():
            obj.assigned_teacher = request.user

        super().save_model(request, obj, form, change)


@admin.register(Enrollment)
class AdminEnrollment(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date')
    search_fields = ('student__name', 'course__title')
    list_filter = ('course', 'enrollment_date')


@admin.register(Result)
class AdminResult(admin.ModelAdmin):
    list_display = ('enrollment', 'marks')
    search_fields = ('enrollment__student__name',)
    list_filter = ('marks',)


admin.site.unregister(User)


@admin.register(User)
class AdminUser(admin.ModelAdmin):
    list_display = ('username', 'email', 'display_groups')
    search_fields = ('username', 'email')
    list_filter = ('groups',)

    def display_groups(self, obj):
        return ", ".join(group.name for group in obj.groups.all())

    display_groups.short_description = 'Groups'