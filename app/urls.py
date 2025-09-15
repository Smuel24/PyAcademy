from django.urls import path
from .views import HomePageView, CoursesPageView, CategoriesPageView, CartPageView, ProfilePageView, CourseIndexView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('Courses/', CoursesPageView.as_view(), name='cursos'),
    path('categorias/', CategoriesPageView.as_view(), name='categories'),
    path('Carrito/', CartPageView.as_view(), name = 'cart'),
    path('Mi Cuenta/', ProfilePageView.as_view(), name = 'profile'),
    path('courses/', CourseIndexView.as_view(), name='course_index'),

]