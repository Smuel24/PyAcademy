from django.urls import path
from .views import (HomePageView, CoursesPageView, CategoryListView, CartPageView, ProfilePageView, 
                    CourseShowView, CategoryDetailView, CartRemoveAllView, add_to_cart, course_content_view, 
                    update_progress, download_certificate, pay_cart)

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('Courses/', CoursesPageView.as_view(), name='cursos'),
    path('categorias/', CategoryListView.as_view(), name='categories'),  
    path('Carrito/', CartPageView.as_view(), name='cart'),
    path('Mi Cuenta/', ProfilePageView.as_view(), name='profile'),
    path('curso/<slug:slug>/', CourseShowView.as_view(), name='course_detail'),
    path('categorias/<slug:slug>/', CategoryDetailView.as_view(), name='category_detail'),
    path('Carrito/add/<str:course_id>', add_to_cart, name = 'cart_add'),
    path('Carrito/removeAll', CartRemoveAllView.as_view(), name = 'cart_removeAll'),
    path('curso/<slug:slug>/', course_content_view, name='course_view'),
    path('curso/<slug:slug>/progreso/', update_progress, name='update_progress'),
    path('certificado/<uuid:cert_id>/', download_certificate, name='download_certificate'),
    path('carrito/pagar/', pay_cart, name='cart_pay'),
]