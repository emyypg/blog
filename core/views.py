from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def nosotros(request):
    return render(request, "nosotros.html")

# def login(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")
#         print("Esto es el correo electronico ingresado por el from login", email)
#         print("Esta es la contraseña ingresada por el from login", password)
#     return render(request, "usuarios/login.html")