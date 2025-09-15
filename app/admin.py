from django.contrib import admin
from .models import Course, Category

# Register your models here.

class CourseInLine(admin.TabularInline):
    model = Course
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug')
    search_fields = ('name', 'description')
    inlines = [CourseInLine]

class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'category', 'certification_price')
    search_fields = ('title',)  # Cambia 'search_field' por 'search_fields' y ponlo como tupla
    list_filter = ('level', 'category')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)