from django import forms
from .models import Post


# class ContactoForm(forms.ModelForm):

#     class Meta:
#         model = Contacto
#         fields = "__all__"


class PostForm(forms.ModelForm):

    class Meta:
        model= Post
        fields = "__all__"