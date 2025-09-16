from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, View
from django.http import HttpResponseRedirect
from .models import Course, Category, Payment
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


# Create your views here.

class HomePageView(TemplateView):
    template_name = 'pages/home.html'


class CategoriesPageView(TemplateView):
    template_name =  'pages/categories.html'


class CartPageView(View):
    template_name = 'pages/cart.html'

    def get(self, request):
        # Cursos disponibles
        products = {}
        for course in Course.objects.all():
            products[str(course.id)] = {
                'name': course.title,
                'price': course.certification_price
            }

        # Cursos en el carrito del usuario
        cart_products = {}
        if request.user.is_authenticated:
            from .models import Cart
            cart_items = Cart.objects.filter(user=request.user).select_related('course')
            for item in cart_items:
                cart_products[str(item.course.id)] = {
                    'name': item.course.title,
                    'price': item.course.certification_price
                }

        context = {
            'title': 'Carrito de compras',
            'products': products,
            'cart_products': cart_products,
        }
        return render(request, self.template_name, context)

class CartRemoveAllView(View):
    template_name = 'pages/cart.html'

    def post(self, request):
        # Mostrar los cursos en el carrito del usuario autenticado
        cart_items = []
        if request.user.is_authenticated:
            from .models import Cart
            cart_items = Cart.objects.filter(user=request.user).select_related('course')
        context = {
            'title': 'Carrito de compras',
            'cart_items': cart_items,
        }
        return render(request, self.template_name, context)

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
        search_query = request.GET.get('q', '')  #
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
        from .models import Category, Course
        category = get_object_or_404(Category, slug=slug)
        courses = Course.objects.filter(category=category)
        context = {
            'category': category,
            'courses': courses,
            'title': f'Categoría: {category.name}',
        }
        return render(request, self.template_name, context)

@login_required
def course_content_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    
    has_paid = Payment.objects.filter(user=request.user, course=course, status='paid').exists()
    if not has_paid:
        return redirect('show_course', slug=slug)
    return render(request, 'course/course_content.html', {'course': course})


@login_required
@require_POST
def add_to_cart(request, course_id):
    # Tu modelo de carrito debería tener user y course
    from .models import Cart, Course
    course = get_object_or_404(Course, id=course_id)
    # Evita duplicados
    cart_item, created = Cart.objects.get_or_create(user=request.user, course=course)
    # Redirige al carrito
    return redirect('cart') 