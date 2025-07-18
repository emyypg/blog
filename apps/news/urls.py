from django.urls import path
from .views import index

urlpatterns = [
    path('', index, name='home'),  # ahora index.html se muestra en la raíz "/"
]
