from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_utilizadores, name='lista_utilizadores'), # Fica vazia ''
    path('utilizadores/novo/', views.gerir_utilizador, name='criar_utilizador'),
    path('utilizadores/editar/<int:id_utilizador>/', views.gerir_utilizador, name='editar_utilizador'),
    path('utilizadores/apagar/<int:id_utilizador>/', views.apagar_utilizador, name='apagar_utilizador'),
]

