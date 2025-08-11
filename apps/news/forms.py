# apps/news/forms.py

from django import forms
from .models import Post, Categoria, Comentario, Contacto
from django.utils import timezone


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'fecha_publicacion', 'imagen_destacada', 'categorias', 'estado']
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
                'type': 'datetime-local',
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 focus:ring-blue-500'
            }),
            'imagen_destacada': forms.FileInput(attrs={
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
            }),
            'categorias': forms.SelectMultiple(attrs={
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 focus:ring-blue-500'
            }),
            'estado': forms.Select(attrs={
                'class': 'shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 focus:ring-blue-500'
            })
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['contenido']
        widgets = {
            'contenido': forms.Textarea(attrs={
                'cols': 80,
                'rows': 5,
                'class': 'form-control shadow appearance-none border rounded-lg w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline focus:ring-2 focus:ring-blue-500',
                'placeholder': 'Edita tu comentario...'
            }),
        }

class ContactoForm(forms.ModelForm):
    asunto = forms.CharField(widget=forms.HiddenInput(), initial='Mensaje de Contacto Web')

    class Meta:
        model = Contacto
        fields = ['nombre', 'correo', 'texto', 'asunto']
        labels = {
            'nombre': 'Tu nombre',
            'correo': 'Tu email',
            'texto': 'Tu mensaje',
        }
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }