from django.db import models
import uuid
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuidd4, editable= False)
    name = models.CharField(max_length = 150)
    description = models.CharField(max_length = 300)
    slug = models.SlugField(unique = True)


class Course(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.CharField(max_length = 250)
    date = models.DateField()
    duration = models.IntegerField()
    certification_price = models.DecimalField()
    slug = models.SlugField(unique = True)
    img = models.ImageField(upload_to='portadas/', null=True, blank=True)
    Category = models.ForeignKey(Category, on_delete = models.CASCADE, related_name= 'cursos')
    Level = (
        ('Basic', 'Basic'), 
        ('Intermediate', 'Intermediate'),
        ('Experienced', 'Experienced'), 

    )

class Module(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.CharField(max_length = 200)
    decripcion = models.CharField()
    order = models.IntegerField()


class Resource(models.model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    title = models.CharField()
    url = models.URLField()
    duration = models.FloatField(nuul = True, blank = True)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='recursos')
    TYPES = (
        ('Video', 'Video'),
        ('PDf', 'PDF'),
    )
    type = models.CharField(max_length=10, choices= TYPES)

class Progreso(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    curso = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='progresos')
    porcentaje = models.FloatField()
    fecha_actualizacion = models.DateTimeField(auto_now=True)



class Payment(models.Model):
    STATES = (
        ('PENDING', 'PENDING'),
        ('PAID', 'PAID'),
        ('FAILED', 'FAILED'),
    )
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    curso = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='pagos')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    date = models.DateTimeField()
    transaction_id = models.CharField(max_length = 100)
    state = models.CharField(max_length = 10, choices = STATES)


class Certification(models.Model):
    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    Payment = models.ForeignKey(Payment, on_delete=models.CASCADE, related_name='certificados')
    unique_code = models.CharField(max_length = 50, unique = True) 
    emition_date = models.DateTimeField()

class User(models.Models):
    id = models.UUIDField(primary_key = True, default = uuid.uuid, editable = False)
    mail = models.EmailField(unique = True)
    password = models.CharField(max_length=128)
    registration_date = models.DateField()
    active = models.BooleanField(default = True)

class Profile(models.Model):
    ROLES = (
        ('Estudent', 'Estudent'),
        ('Instructor', 'Instructor'),
        ('Admin', 'admin'),
    )

    id = models.UUIDField(primary_key = True, default = uuid.uuid4, editable = False)
    name = models.CharField(max_length = 50)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=20, choices=ROLES)