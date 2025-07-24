from django.urls import path
from apps.news import views
from .views import *

app_name = 'news'  # Define el nombre de la aplicación para el espacio de nombres

urlpatterns = [
    path('', index, name='home'),  # ahora index.html se muestra en la raíz "/"
    path('post_detail/<int:pk>/', post_detail, name='post_detail'),  # Detalle del post
]
