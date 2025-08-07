from django.contrib import admin
from django.urls import path, include  # 👈 importamos include
from django.conf.urls.static import static
from django.conf import settings
from .views import nosotros

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.news.urls')),  # 👈 conectamos a tu app
    path("usuarios/", include("apps.usuarios.urls")),  # 👈 conectamos a tu app de usuarios
    path('nosostros/', nosotros, name='nosotros'),
]

# Configuración para servir archivos de medios durante el desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
