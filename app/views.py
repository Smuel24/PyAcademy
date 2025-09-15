from django.shortcuts import render, redirect, get_list_or_404
from django.views.generic import TemplateView, ListView, View
from .models import Course

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