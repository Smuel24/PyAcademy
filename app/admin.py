from django.contrib import admin
from .models import Course, Category



# Register your models here.
admin.site.register(Course)
admin.site.register(Category)

class CourseInLine(admin.TabularInline):
    model = Course
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug')
    search_fields = ('name', 'description')
    inlines = [CourseInLine]

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'category', 'certiication_price')
    search_field = ('title')
    list_filter = ('level', 'category')

admin.site.register(Course, CourseAdmin)  


    