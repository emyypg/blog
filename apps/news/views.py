from django.shortcuts import render

# Vista principal del sitio (usa index.html que extiende de base.html)
def index(request):
    return render(request, 'news/index.html')
