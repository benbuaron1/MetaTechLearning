from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(UserProfile)
admin.site.register(UserType)
admin.site.register(StudentTeacherLesson)
admin.site.register(Test)
admin.site.register(TestExecuted)
admin.site.register(Question)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Subject)

