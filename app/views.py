from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, View
from django.http import HttpResponseRedirect
from .models import Course, Category

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class CategoriesPageView(TemplateView):
    template_name =  'pages/categories.html'


class CartPageView(View):
    template_name = 'pages/cart.html'

    def get(self, request):
        cart_courses = {}
        cart_courses_data = request.session.get('cart_courses_data', {})

        for key, course in Course.objects.in_bulk(cart_courses_data.keys()).items():
            cart_courses[key] = course

        context = {
            'title': 'Carrito de compras',
            'cart_courses': cart_courses,
        }
        return render(request, self.template_name, context)

    def post(self, request, course_id):
        cart_courses_data = request.session.get('cart_courses_data', {})  # <--- usa el mismo nombre
        cart_courses_data[str(course_id)] = course_id
        request.session['cart_courses_data'] = cart_courses_data  # <--- usa el mismo nombre

        return redirect('cart')    


class CartRemoveAllView(View):
    def post(self, request):
        if 'cart_courses_data' in request.session:
            del request.session['cart_courses_data']

        return redirect('cart')


class ProfilePageView(TemplateView):
    template_name = 'pages/Profile.html'

    

    

class CoursesPageView(TemplateView):
    template_name = 'pages/courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['title'] = "Todos los cursos"
        context['query'] = ""
        return context


class CourseShowView(View):
    template_name = 'course/showcourse.html'

    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        context = {'course': course}
        return render(request, self.template_name, context)
                
                

class CategoryListView(View):
    template_name = 'pages/categories.html'  

    def get(self, request):
        search_query = request.GET.get('q', '')  # Agrega el parámetro de búsqueda
        if search_query:
            categories = Category.objects.filter(
                name__icontains=search_query
            ) | Category.objects.filter(
                description__icontains=search_query
            )
        else:
            categories = Category.objects.all()
        context = {
            'categories': categories,
            'title': 'Todas las Categorías',
            'search_query': search_query
        }
        return render(request, self.template_name, context)


class CategoryDetailView(View):
    template_name = 'category/category_detail.html'
    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        # Si tienes la relación, úsala así:
        # courses = category.courses.all()
        context = {
            'category': category,
            # 'courses': courses, # descomenta si tienes la relación
            'title': f'Categoría: {category.name}',
        }