from django.urls import path
from apps.news import views
from .views import *

app_name = 'news'  # Define el nombre de la aplicación para el espacio de nombres

urlpatterns = [
    path('', index, name='home'),  # ahora index.html se muestra en la raíz "/"
    path('post/<int:pk>/', views.post_detail, name='post_detail'),  # Detalle del post
    path('add_post', agregar_post, name='agregar_post'),
    path('<int:pk>/editar_post', editar_post, name='editar_post'),
    path('<int:pk>/delete_post', eliminar_post, name='eliminar_post'),
    path('comentario', Comentar_Post, name='comentar'),
    path('<int:pk>/editar_comentario/', EditarComentario.as_view(), name='editar_cometario'),
    path('<int:pk>/eliminar_comentario/', CommentDeleteView.as_view(), name='eliminar_comentario'),
]
