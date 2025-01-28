from django.urls import path
from students.views import StudentsViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentsViewSet

router = DefaultRouter()
router.register(r'students', StudentsViewSet, basename='students')


urlpatterns = [
    path('', include(router.urls)),

]