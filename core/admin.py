from django.contrib import admin
from .models import Student,Enrollment,Course,Result

# Register your models here.
admin.site.register(Student)
admin.site.register(Enrollment)
admin.site.register(Course)
admin.site.register(Result)