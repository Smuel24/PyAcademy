from django.contrib import admin
from .models import Course



# Register your models here.
admin.site.register(Course)

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'category', 'certiication_price')
    search_field = ('title')
    list_filter = ('level', 'category')

admin.site.register(Course, CourseAdmin)  
