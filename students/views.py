from django.shortcuts import render
from rest_framework import viewsets, mixins, generics
from students.models import Student, Course


from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from students.serializers import UserSerializer, StudentSerializer , CourseSerializer
from students.models import Student

class StudentsViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data["username"])
        return Response({
            "id": user.id,
            "username": user.username
        })

# Tizimga kirish
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=400)

# Talabalar ro‘yxati va tafsilotlari
class StudentListView(generics.ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

class StudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.request.user.is_staff:  # Admin barcha talabalarga kirishi mumkin
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Student.objects.all()  # Admin barcha talabalarga kirishi mumkin
        return Student.objects.filter(user=self.request.user)  #

# Courses View
class CourseViewSet(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)  # GET /courses/<id>/
        return self.list(request, *args, **kwargs)         # GET /courses/

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)       # POST /courses/

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)       # PUT /courses/<id>/

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)