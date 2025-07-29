from django.shortcuts import render
import random # ordenar aleatoriamente a los integrantes del equipo

def home(request):
    return render(request, "home.html")

def nosotros(request):
    # ordenar aleatoriamente a los integrantes del equipo
    integrantes = [
        {'nombre': 'bertran, nelson', 'portfolio': 'https://portfolio-neelbit.netlify.app/', 'github': 'https://github.com/NeelBit'},
        {'nombre': 'Cardozo, Ricardo', 'portfolio': '#', 'github': 'https://github.com/RickyRicardo19'},
        {'nombre': 'Carlos, Eduardo Gomez', 'portfolio': '#', 'github': 'https://github.com/gcarloseduardo'},
        {'nombre': 'Puente Gonzalez, Emily', 'portfolio': '#', 'github': 'https://github.com/emyypg'},
        {'nombre': 'Velazco, Carlos Ariel', 'portfolio': '#', 'github': 'https://github.com/carvelaz'},
    ]
    
    random.shuffle(integrantes)  # Mezclar la lista de integrantes
    return render(request, 'nosotros.html', {'integrantes': integrantes})


