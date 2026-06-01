from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    # Pedidos CRUD
    path('pedidos/', views.list_pedidos_exame, name='list_pedidos_exame'),
    path('pedidos/novo/', views.register_pedido_exame, name='register_pedido_exame'),
    path('pedidos/<int:pk>/editar/', views.edit_pedido_exame, name='edit_pedido_exame'),
    path('pedidos/<int:pk>/eliminar/', views.delete_pedido_exame, name='delete_pedido_exame'),
    path('pedidos/<int:pk>/upload/', views.upload_ficheiro, name='upload_ficheiro'),

    # Utilizadores CRUD
    path('utilizadores/', views.list_utilizadores, name='list_utilizadores'),
    path('utilizadores/novo/', views.register_utilizador, name='register_utilizador'),
    path('utilizadores/<int:pk>/editar/', views.edit_utilizador, name='edit_utilizador'),
    path('utilizadores/<int:pk>/eliminar/', views.delete_utilizador, name='delete_utilizador'),

    # Dúvidas CRUD
    path('duvidas/', views.list_duvidas, name='list_duvidas'),
    path('duvidas/novo/', views.register_duvida, name='register_duvida'),
    path('duvidas/<int:pk>/', views.detail_duvida, name='detail_duvida'),
    path('duvidas/<int:pk>/editar/', views.edit_duvida, name='edit_duvida'),
    path('duvidas/<int:pk>/eliminar/', views.delete_duvida, name='delete_duvida'),

    # Placeholder routes for legacy templates/navigation
    path('doentes/', views.list_doentes, name='list_doentes'),
    path('consultas/', views.list_consultas, name='list_consultas'),
    path('doentes/novo/', views.register_doente, name='register_doente'),
    path('consultas/novo/', views.register_consulta, name='register_consulta'),
]
