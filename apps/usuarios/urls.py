from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Registro

app_name = 'usuarios'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('registro/', Registro.as_view(), name="registro"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]