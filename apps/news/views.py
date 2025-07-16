from django.shortcuts import render

def index(request):
    return render(request, 'news/index.html')

def landing(request):
    return render(request, 'news/landing.html') 

def index(request):
    return render(request, 'news/index.html')
