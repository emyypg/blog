from django.contrib import admin
from django.urls import path, include  # 👈 importamos include
from django.conf import settings
from django.conf.urls.static import static
from apps.news import views  # Asegúrate de importar tus vistas

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.news.urls')),  # 👈 conectamos a tu app
]

# Configuración para servir archivos de medios durante el desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
