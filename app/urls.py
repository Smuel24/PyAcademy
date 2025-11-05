from django.urls import path
from . import views
from .views import (
    HomePageView, 
    CoursesPageView, 
    CategoryListView, 
    CartPageView, 
    ProfilePageView, 
    CourseShowView, 
    CategoryDetailView, 
    CartRemoveAllView, 
    add_to_cart, 
    course_content_view, 
    update_progress_video, 
    download_certificate, 
    pay_cart, 
    my_courses, 
    generate_certificate_pdf,
    news_view
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('Courses/', CoursesPageView.as_view(), name='cursos'),
    path('categorias/', CategoryListView.as_view(), name='categories'),  
    path('Carrito/', CartPageView.as_view(), name='cart'),
    path('Mi Cuenta/', ProfilePageView.as_view(), name='profile'),
    path('curso/<slug:slug>/contenido/', course_content_view, name='course_content'),
    path('curso/<slug:slug>/', CourseShowView.as_view(), name='course_detail'),
    path('categorias/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('Carrito/add/<str:course_id>', add_to_cart, name='cart_add'),
    path('Carrito/removeAll', CartRemoveAllView.as_view(), name='cart_removeAll'),
    path('curso/<slug:slug>/video/<uuid:resource_id>/progreso/', update_progress_video, name='update_progress_video'),
    path('certificado/<uuid:cert_id>/', download_certificate, name='download_certificate'),
    path('carrito/pagar/', pay_cart, name='cart_pay'),
    path('mis-cursos/', my_courses, name='my_courses'),
    path('curso/<uuid:course_id>/certificado_pdf/', generate_certificate_pdf, name='generate_certificate_pdf'),
    path('api-demo/', views.api_demo_view, name='api_demo'),
    path('noticias/', views.news_view, name='news'),
    path('noticias/', views.news_view, name='news'),
]