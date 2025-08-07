from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import RegistroForm

class Registro(CreateView):
    form_class = RegistroForm
    success_url = reverse_lazy('news:home')  # Redirige al home después del registro
    template_name = 'usuarios/registro.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # Loguea automáticamente al usuario recién registrado
        return response
