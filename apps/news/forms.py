from django import forms
from .models import Post, Categoria
from django.utils import timezone


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'fecha_publicacion', 'imagen_destacada', 'categorias', 'estado'] # Añade 'estado' también
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Título del post'
            }),
            'contenido': forms.Textarea(attrs={
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 focus:ring-blue-500 h-32',
                'placeholder': 'Contenido del post'
            }),
            'fecha_publicacion': forms.DateTimeInput(attrs={
                'type': 'datetime-local', # Esto habilita el selector de fecha y hora del navegador
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 focus:ring-blue-500'
            }),
            'imagen_destacada': forms.FileInput(attrs={
                # Clases de Tailwind para inputs de tipo file
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
            }),
            'categorias': forms.SelectMultiple(attrs={
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 focus:ring-blue-500'
            }),
            'estado': forms.Select(attrs={
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 focus:ring-blue-500'
            })
        }