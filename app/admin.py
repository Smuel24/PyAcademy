from django.contrib import admin
import nested_admin
from .models import Course, Category, Module, Resource, Progress, Payment, Certification, Profile

# Register your models here.

class ResourceInline(nested_admin.NestedTabularInline):
    model = Resource
    extra = 1


class ModuleInline(nested_admin.NestedTabularInline):  # <- corregido nombre y herencia
    model = Module
    extra = 1
    inlines = [ResourceInline]

class CourseAdmin(nested_admin.NestedModelAdmin):
    list_display = ('title', 'level', 'category', 'certification_price')
    search_fields = ('title',)
    list_filter = ('level', 'category')
    inlines = [ModuleInline]

class CourseInline(admin.TabularInline):
    model = Course
    extra = 1

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'slug')
    search_fields = ('name', 'description')
    inlines = [CourseInline]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Module)
admin.site.register(Resource)
admin.site.register(Progress)
admin.site.register(Payment)
admin.site.register(Certification)
admin.site.register(Profile)