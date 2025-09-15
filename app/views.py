from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, View
from django.http import HttpResponseRedirect
from .models import Course, Category

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class CoursesPageView(TemplateView):
    template_name = 'pages/courses.html'


class CategoriesPageView(TemplateView):
    template_name =  'pages/categories.html'


class CartPageView(TemplateView):
    template_name = 'pages/cart.html'


class ProfilePageView(TemplateView):
    template_name = 'pages/Profile.html'

    
class CourseIndexView(View):
    template_name = 'course/indexcourse.html'

    def get(self, request):
        viewData = {}
        viewData['title'] = "Todos los Cursos"
        viewData['courses'] = Course.objects.all()
        return render(request, self.template_name, viewData)



class CoureShowView(View):
    Template_name = 'course/showcourse.html'

    def get(self, request): 

            try:
                course_id = int(id)
                if course_id < 1:
                    raise ValueError("course id must be 1 or greater")
                course = get_object_or_404(Course, pk = course_id)
            except(ValueError, IndexError):
                return HttpResponseRedirect
                
                

class CategoryListView(View):
    template_name = 'category/categories.html'

    def get(self, request):
        categories = Category.objects.all()
        context = {
            'categories': categories,
            'title': 'Todas las Categorías'
        }
        return render(request, self.template_name, context)

class CategoryDetailView(View):
    template_name = 'category/category_detail.html'

    def get(self, request, slug):
        category = get_object_or_404(Category, slug=slug)
        # Los cursos de la categoría se acceden por: category.cursos.all()
        courses = category.cursos.all()
        context = {
            'category': category,
            'courses': courses,
            'title': f'Categoría: {category.name}'
        }
        return render(request, self.template_name, context)
            