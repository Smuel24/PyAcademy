from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, ListView, View
from django.http import HttpResponseRedirect
from .models import Course, Category, Payment, Progress, Certification, Cart, User
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib.auth import authenticate, login 
from django.utils.decorators import method_decorator
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

@method_decorator(login_required, name='dispatch')
class ProfilePageView(TemplateView):
    template_name = 'pages/Profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "user": request.user,
            "success": "",
            "error": "",
        })

    def post(self, request, *args, **kwargs):
        user = request.user
        username = request.POST.get("username", user.username)
        first_name = request.POST.get("first_name", user.first_name)
        last_name = request.POST.get("last_name", user.last_name)
        email = request.POST.get("email", user.email)

        error = ""
        success = ""

        # Validaciones simples
        if not username or not first_name or not last_name or not email:
            error = "Todos los campos son obligatorios."
        elif username != user.username and user.__class__.objects.filter(username=username).exists():
            error = "El usuario ya existe."
        elif email != user.email and user.__class__.objects.filter(email=email).exists():
            error = "El correo ya está registrado."
        else:
            user.username = username
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            success = "¡Datos actualizados correctamente!"

        return render(request, self.template_name, {
            "user": user,
            "success": success,
            "error": error,
        })
    

class CoursesPageView(TemplateView):
    template_name = 'pages/courses.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        context['title'] = "Todos los cursos"
        context['query'] = ""
        return context


class CourseShowView(View):
    def get(self, request, slug):
        course = get_object_or_404(Course, slug=slug)
        user_has_course = False
        if request.user.is_authenticated:
            user_has_course = Payment.objects.filter(
                usuario=request.user,
                curso=course,
                state='PAID'
            ).exists()
        return render(request, 'course/showcourse.html', {
            'course': course,
            'user_has_course': user_has_course
        })
                
                

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
@require_POST
def add_to_cart(request, course_id):
    # Tu modelo de carrito debería tener user y course
    from .models import Cart, Course
    course = get_object_or_404(Course, id=course_id)
    # Evita duplicados
    cart_item, created = Cart.objects.get_or_create(user=request.user, course=course)
    # Redirige al carrito
    return redirect('cart') 



@login_required
def course_content_view(request, slug):
    course = get_object_or_404(Course, slug=slug)
    progress_obj, created = Progress.objects.get_or_create(
        curso=course,
        usuario=request.user,
        defaults={'porcentaje': 0}
    )
    show_certificate = progress_obj.porcentaje >= 100
    certificate = None
    if show_certificate:
        certificate = Certification.objects.filter(curso=course, usuario=request.user).first()
    return render(request, 'course/course_content.html', {   # <-- usa el template correcto AQUÍ
        'course': course,
        'progress': progress_obj.porcentaje,
        'show_certificate': show_certificate,
        'certificate': certificate
    })

@login_required
def update_progress(request, slug):
    course = get_object_or_404(Course, slug=slug)
    if request.method == 'POST':
        progress_obj, created = Progress.objects.get_or_create(
            curso=course,
            usuario=request.user,
            defaults={'porcentaje': 0}
        )
        nuevo_porcentaje = float(request.POST.get('porcentaje', 0))
        progress_obj.porcentaje = min(100, max(0, nuevo_porcentaje))
        progress_obj.save()
        if progress_obj.porcentaje >= 100:
            payment = Payment.objects.filter(curso=course, usuario=request.user, state='PAID').first()
            if payment:
                from .models import Certification
                if not Certification.objects.filter(payment=payment).exists():
                    import random
                    unique_code = f"CERT-{random.randint(100000,999999)}"
                    Certification.objects.create(
                        payment=payment,
                        unique_code=unique_code,
                        emition_date=timezone.now()
                    )
        return redirect('course_view', slug=slug)
    


@login_required
def download_certificate(request, cert_id):
    certificate = get_object_or_404(Certification, id=cert_id)
    return render(request, 'course/certificate.html', {
        'certificate': certificate,
        'user': request.user,
        'course': certificate.payment.curso
    })


@login_required
def pay_cart(request):
    if request.method == 'POST':
        cart_items = Cart.objects.filter(user=request.user).select_related('course')
        for item in cart_items:
            Payment.objects.create(
                curso=item.course,
                usuario=request.user,
                amount=item.course.certification_price,
                date=timezone.now(),
                transaction_id=f"TX-{timezone.now().timestamp()}-{item.course.id}",
                state='PAID'
            )
        cart_items.delete()
        return redirect('cart')
    

@login_required
def my_courses(request):
    # Buscar todos los pagos exitosos del usuario
    pagos = Payment.objects.filter(usuario=request.user, state='PAID').select_related('curso')
    # Extraer los cursos únicos de esos pagos
    cursos = list({pago.curso.id: pago.curso for pago in pagos}.values())
    context = {
        'cursos': cursos,
        'title': 'Mis Cursos'
    }
    return render(request, 'pages/my_courses.html', context)


def login_view(request):
    error = ""
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")         
            error = "Usuario o contraseña incorrectos"
    return render(request, "pages/login.html", {"error": error})



def register_view(request):
    error = ""
    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]

        if password != password2:
            error = "Las contraseñas no coinciden."
        elif User.objects.filter(username=username).exists():
            error = "El usuario ya existe."
        elif User.objects.filter(email=email).exists():
            error = "El correo ya está registrado."
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return redirect("home")

    return render(request, "pages/register.html", {"error": error})