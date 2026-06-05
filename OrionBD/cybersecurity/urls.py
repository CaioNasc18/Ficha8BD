from django.urls import path
from . import views

urlpatterns = [
    # =====================================================================
    # 1. ROTA PRINCIPAL (MENU DE ENTRADA)
    # =====================================================================
    path('', views.menu_principal, name='menu_principal'), # Agora a página inicial é o menu.html

    # =====================================================================
    # 2. ROTAS DOS UTILIZADORES (MANTIDAS E AJUSTADAS)
    # =====================================================================
    path('utilizadores/', views.lista_utilizadores, name='lista_utilizadores'), # Movido de '' para 'utilizadores/'
    path('utilizadores/novo/', views.gerir_utilizador, name='criar_utilizador'),
    path('utilizadores/editar/<int:id_utilizador>/', views.gerir_utilizador, name='editar_utilizador'),
    path('utilizadores/apagar/<int:id_utilizador>/', views.apagar_utilizador, name='apagar_utilizador'),

    # =====================================================================
    # 3. ROTAS DOS PEDIDOS / REQUESTS (NOVAS)
    # =====================================================================
    # Ajuste os nomes das funções (views.listar_pedidos, etc.) se tiver usado nomes diferentes no seu views.py
    path('pedidos/', views.listar_pedidos, name='lista_pedidos'),
    path('pedidos/novo/', views.gerir_pedido, name='criar_pedido'),
    path('pedidos/editar/<int:id_pedido>/', views.gerir_pedido, name='editar_pedido'),
    path('pedidos/apagar/<int:id_pedido>/', views.apagar_pedido, name='apagar_pedido'),

    # Empresas

    # NOVO: Rotas para o CRUD de Empresas
   # Em cybersecurity/urls.py (Linha 30)
    path('empresas/', views.listar_empresas, name='empresas'), #
    path('empresas/nova/', views.criar_empresa_view, name='criar_empresa'),
    path('empresas/editar/<int:id_empresa>/', views.editar_empresa_view, name='editar_empresa'),
    path('empresas/apagar/<int:id_empresa>/', views.apagar_empresa_view, name='apagar_empresa'),
]
