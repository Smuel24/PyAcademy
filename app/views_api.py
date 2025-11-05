from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Avg, Count
from django.contrib.auth.models import User
from .models import Course, Progress
from .serializers import CourseSerializer, StudentProgressSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """API REST para gestionar cursos"""
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class StudentProgressViewSet(viewsets.ModelViewSet):
    """API REST para ver progreso de estudiantes"""
    queryset = Progress.objects.all()
    serializer_class = StudentProgressSerializer


@api_view(['GET'])
def courses_simple_api(request):
    """GET /api/courses-simple/"""
    try:
        courses = Course.objects.all().values(
            'id', 'title', 'level', 'duration'
        )
        return Response({
            'status': 'success',
            'total': courses.count(),
            'courses': list(courses)
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def students_grades_api(request):
    """GET /api/students-grades/"""
    try:
        students = User.objects.filter(
            progresos__isnull=False
        ).annotate(
            courses_taken=Count('progresos__curso', distinct=True),
            average_progress=Avg('progresos__porcentaje')
        ).values(
            'id',
            'first_name',
            'last_name',
            'email',
            'courses_taken',
            'average_progress'
        ).distinct()
        
        students_list = []
        for student in students:
            students_list.append({
                'id': student['id'],
                'name': f"{student['first_name']} {student['last_name']}",
                'email': student['email'],
                'courses_taken': student['courses_taken'],
                'average_progress': round(student['average_progress'], 2) if student['average_progress'] else 0
            })
        
        return Response({
            'status': 'success',
            'total': len(students_list),
            'students': students_list
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def promotions_api(request):
    """GET /api/promotions/"""
    try:
        courses = Course.objects.all().values('id', 'title', 'certification_price')
        
        promotions_list = []
        for course in courses:
            original_price = course['certification_price'] if course['certification_price'] else 0
            discount_price = round(original_price * 0.8, 2)
            
            promotions_list.append({
                'id': course['id'],
                'title': course['title'],
                'original_price': original_price,
                'discount_price': discount_price,
                'discount_percentage': 20
            })
        
        return Response({
            'status': 'success',
            'total': len(promotions_list),
            'promotions': promotions_list
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def featured_mascots_api(request):
    """GET /api/featured-mascots/"""
    mascots = [
        {
            'id': 1,
            'name': 'Rex',
            'species': 'Perro',
            'breed': 'Labrador',
            'age': 3,
            'available': True
        },
        {
            'id': 2,
            'name': 'Whiskers',
            'species': 'Gato',
            'breed': 'Siamés',
            'age': 2,
            'available': True
        },
        {
            'id': 3,
            'name': 'Tweety',
            'species': 'Loro',
            'breed': 'Guacamayo',
            'age': 5,
            'available': True
        }
    ]
    
    return Response({
        'status': 'success',
        'total': len(mascots),
        'mascots': mascots
    }, status=status.HTTP_200_OK)


