from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class CoursesPageView(TemplateView):
    template_name = 'pages/courses.html'


class CategoriesPageView(TemplateView):
    template_name =  'pages/categories.html'

    


    

