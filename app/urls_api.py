from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views_api import (
    CourseViewSet,
    StudentProgressViewSet,
    courses_simple_api,
    students_grades_api,
    promotions_api,
    featured_mascots_api
)

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='course')
router.register(r'student-progress', StudentProgressViewSet, basename='progress')

urlpatterns = [
    path('', include(router.urls)),
    path('courses-simple/', courses_simple_api, name='courses_simple'),
    path('students-grades/', students_grades_api, name='students_grades'),
    path('promotions/', promotions_api, name='promotions'),
    path('featured-mascots/', featured_mascots_api, name='featured_mascots'),
    
]