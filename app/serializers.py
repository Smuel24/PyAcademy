from rest_framework import serializers
from .models import Course, Progress
from django.contrib.auth.models import User


class CourseSerializer(serializers.ModelSerializer):
    """Serializador para Cursos"""
    instructor_name = serializers.CharField(source='instructor.user.get_full_name', read_only=True)
    
    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'price',
            'level',
            'instructor_name',
            'created_at',
            'is_active'
        ]


class StudentProgressSerializer(serializers.ModelSerializer):
    """Serializador para Progreso de Estudiantes"""
    student_name = serializers.CharField(source='user.get_full_name', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)
    
    class Meta:
        model = Progress
        fields = [
            'id',
            'student_name',
            'course_title',
            'percentage',
            'resources_viewed',
            'created_at'
        ]