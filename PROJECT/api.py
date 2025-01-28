from rest_framework import routers

from students import views



router = routers.DefaultRouter()


router.register('Students', views.StudentsViewSet)
router.register('Course', views.CourseViewSet)