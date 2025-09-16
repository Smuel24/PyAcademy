from django.db import models
import uuid
from django.contrib.auth.models import User

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    description = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=250)
    date = models.DateField()
    duration = models.IntegerField()
    certification_price = models.DecimalField(max_digits=8, decimal_places=2)
    slug = models.SlugField(unique=True)
    img = models.ImageField(upload_to='portadas/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cursos')
    LEVELS = (
        ('Basic', 'Basic'), 
        ('Intermediate', 'Intermediate'),
        ('Experienced', 'Experienced'), 
    )
    level = models.CharField(max_length=15, choices=LEVELS)

class Module(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=300)
    order = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')

class Resource(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)
    url = models.URLField()
    duration = models.FloatField(null=True, blank=True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='resources')
    TYPES = (
        ('Video', 'Video'),
        ('PDF', 'PDF'),
    )
    type = models.CharField(max_length=10, choices=TYPES)

class Progress(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    curso = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progresos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progresos')
    porcentaje = models.FloatField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)

class Payment(models.Model):
    STATES = (
        ('PENDING', 'PENDING'),
        ('PAID', 'PAID'),
        ('FAILED', 'FAILED'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    curso = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='pagos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pagos')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField()
    transaction_id = models.CharField(max_length=100)
    state = models.CharField(max_length=10, choices=STATES)

class Certification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='certificados')
    unique_code = models.CharField(max_length=50, unique=True) 
    emition_date = models.DateTimeField()

class Profile(models.Model):
    ROLES = (
        ('Estudent', 'Estudent'),
        ('Instructor', 'Instructor'),
        ('Admin', 'Admin'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)