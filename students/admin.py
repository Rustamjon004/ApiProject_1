from django.contrib import admin
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from students.models import Student, Course

admin.site.register(Token)
admin.site.register(Student)

admin.site.register(Course)

# Register your models here.
