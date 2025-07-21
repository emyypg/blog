from django.contrib import admin
from django.urls import path, include  # 👈 importamos include
from django.conf.urls.static import static
from apps.news import views  # Asegúrate de importar tus vistas
from appusuarios import views  # Importa las vistas de tu app de usuarios
from django.contrib.auth import views as auth
from django.urls import reverse_lazy 
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.news.urls')),  # 👈 conectamos a tu app
    path('login/', auth.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/',auth.LogoutView.as_view() , name='logout'),
    path("usuarios/", include("appusuarios.urls")),
    

]

# Configuración para servir archivos de medios durante el desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
