from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from app.views import login_view, register_view, api_demo_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/', include('nested_admin.urls')),
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/', include('app.urls_api')),
    path('api-demo/', api_demo_view, name='api_demo'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
]

urlpatterns += i18n_patterns(
    path('', include('app.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)