from rest_framework import serializers


from .models import Student, Course
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class CourseCreateSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(queryset=Student.objects.all(), many=True)

    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'students']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'