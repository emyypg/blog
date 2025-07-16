from django.urls import path
from .views import landing, index

urlpatterns = [
    path('', landing, name='landing'),
    path('home/', index, name='home'),
]
