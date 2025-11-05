from django.test import TestCase, Client
from django.utils import translation
from django.utils.translation import gettext as _
from django.contrib.auth.models import User


# ============================================
# PRUEBA 1: Internacionalización (Idioma)
# ============================================

class TestI18nTranslation(TestCase):
    """Prueba que las traducciones de idioma funcionan correctamente"""
    
    def test_spanish_english_translation(self):
        """
        Verifica que al cambiar de idioma, las cadenas se traducen correctamente
        
        ✅ Prueba 1:
        - Activar idioma español
        - Verificar que "Cursos" se traduce a "Cursos"
        
        ✅ Prueba 2:
        - Activar idioma inglés
        - Verificar que "Cursos" se traduce a "Courses"
        """
        # Activar español
        translation.activate('es')
        spanish_cursos = _("Cursos")
        spanish_categorias = _("Categorías")
        spanish_carrito = _("Carrito")
        
        self.assertEqual(spanish_cursos, "Cursos")
        self.assertEqual(spanish_categorias, "Categorías")
        self.assertEqual(spanish_carrito, "Carrito")
        
        # Activar inglés
        translation.activate('en')
        english_cursos = _("Cursos")
        english_categorias = _("Categorías")
        english_carrito = _("Carrito")
        
        self.assertEqual(english_cursos, "Courses")
        self.assertEqual(english_categorias, "Categories")
        self.assertEqual(english_carrito, "Cart")
        
        # Desactivar
        translation.deactivate()


# ============================================
# PRUEBA 2: Autenticación de Usuarios
# ============================================

class TestUserAuthentication(TestCase):
    """Prueba que el sistema de autenticación de usuarios funciona"""
    
    def setUp(self):
        """
        Configuración inicial para cada prueba
        - Crea un cliente HTTP para simular peticiones
        - Crea un usuario de prueba
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_user_login_success(self):
        """
        ✅ Prueba 1: Verificar que un usuario puede iniciar sesión correctamente
        
        - Usuario: testuser
        - Contraseña: testpass123
        - Esperado: Login exitoso (True)
        """
        login_success = self.client.login(
            username='testuser',
            password='testpass123'
        )
        self.assertTrue(login_success, "El usuario no pudo iniciar sesión")
    
    def test_user_login_failure(self):
        """
        ✅ Prueba 2: Verificar que NO se puede iniciar sesión con contraseña incorrecta
        
        - Usuario: testuser
        - Contraseña: wrongpassword (incorrecta)
        - Esperado: Login fallido (False)
        """
        login_success = self.client.login(
            username='testuser',
            password='wrongpassword'
        )
        self.assertFalse(login_success, "Login debería haber fallado con contraseña incorrecta")
    
    def test_user_creation(self):
        """
        ✅ Prueba 3: Verificar que se puede crear un nuevo usuario
        
        - Crear usuario: newuser
        - Email: new@example.com
        - Esperado: Usuario existe en la base de datos
        """
        new_user = User.objects.create_user(
            username='newuser',
            email='new@example.com',
            password='newpass123'
        )
        
        self.assertTrue(User.objects.filter(username='newuser').exists())
        self.assertEqual(new_user.email, 'new@example.com')
    
    def test_user_properties(self):
        """
        ✅ Prueba 4: Verificar que las propiedades del usuario se guardaron correctamente
        
        - Recuperar usuario: testuser
        - Verificar: email, username, is_active
        """
        user = User.objects.get(username='testuser')
        
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.username, 'testuser')
        self.assertTrue(user.is_active)