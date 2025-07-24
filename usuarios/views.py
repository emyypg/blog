from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegistroForm

class Registro(CreateView):
    form_class = RegistroForm
    success_url = reverse_lazy('usuarios:login')  # Redirige al login después del registro
    template_name = 'usuarios/registro.html'  # Asegúrate de que esta plantilla exista

