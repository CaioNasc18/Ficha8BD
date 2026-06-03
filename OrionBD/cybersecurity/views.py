from django.shortcuts import render, redirect
from django.http import Http404
from .basedados import (
    # Métodos dos Utilizadores
    listar_todos_utilizadores, obtener_utilizador_por_id, criar_utilizador,
    atualizar_utilizador, eliminar_utilizador, listar_tipos_utilizador, listar_empresas,
    # Métodos dos Pedidos (Requests)
    listar_tipos_pedido, criar_pedido, listar_todos_pedidos, obter_pedido_por_id,
    atualizar_pedido, eliminar_pedido, adicionar_ficheiro_pedido, listar_ficheiros_de_pedido
)

# =====================================================================
# 1. NAVEGAÇÃO / MENU PRINCIPAL
# =====================================================================

def menu_principal(request):
    """Renderiza a página inicial com as opções de navegação do sistema"""
    return render(request, 'utilizadores/menu.html')


# =====================================================================
# 2. GESTÃO DE UTILIZADORES (USERS)
# =====================================================================

def lista_utilizadores(request):
    """Renderiza a listagem de todos os utilizadores"""
    utilizadores = listar_todos_utilizadores()
    return render(request, 'utilizadores/lista.html', {'utilizadores': utilizadores})


def gerir_utilizador(request, id_utilizador=None):
    """Gere a criação e a edição de um utilizador"""
    utilizador = None
    
    if id_utilizador:
        utilizador = obtener_utilizador_por_id(id_utilizador)
        if not utilizador:
            raise Http404("Utilizador não encontrado.")
        utilizador['id_Utilizador'] = utilizador.get('id_Utilizador') or utilizador.get('id_utilizador')

    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        telephone = request.POST.get('telephone')
        active = True if request.POST.get('active') == 'on' else False
        id_tipo = request.POST.get('id_tipo')
        id_empresa = request.POST.get('id_empresa')

        if id_utilizador:
            atualizar_utilizador(id_utilizador, email, name, telephone, active, id_tipo, id_empresa)
        else:
            password = request.POST.get('password')
            criar_utilizador(email, password, name, telephone, active, id_tipo, id_empresa)
            
        return redirect('lista_utilizadores')

    tipos = listar_tipos_utilizador()
    empresas = listar_empresas()

    return render(request, 'utilizadores/formulario.html', {
        'utilizador': utilizador,
        'tipos': tipos,
        'empresas': empresas
    })


def apagar_utilizador(request, id_utilizador):
    """Remove um utilizador do sistema"""
    eliminar_utilizador(id_utilizador)
    return redirect('lista_utilizadores')


# =====================================================================
# 3. GESTÃO DE PEDIDOS (REQUESTS)
# =====================================================================

def listar_pedidos(request):
    """Renderiza a listagem de todos os pedidos reais vindos do banco de dados"""
    pedidos = listar_todos_pedidos() 
    return render(request, 'utilizadores/requestlist.html', {'pedidos': pedidos})


def gerir_pedido(request, id_pedido=None):
    """Trata a visualização, criação e edição de pedidos com chaves estrangeiras de utilizadores"""
    tipos_reais = listar_tipos_pedido()
    utilizadores_reais = listar_todos_utilizadores() # <-- Carrega os utilizadores da BD
    
    pedido_existente = None
    ficheiros_anexados = []
    
    if id_pedido:
        pedido_existente = obter_pedido_por_id(id_pedido)
        if not pedido_existente:
            raise Http404("Pedido não encontrado.")
        ficheiros_anexados = listar_ficheiros_de_pedido(id_pedido)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        status = request.POST.get('status')
        id_tipo_pedido = request.POST.get('id_tipo_pedido') or None
        
        # Captura os IDs dos novos menus drop-down (se vazios, ficam None/Null)
        creator_id = request.POST.get('creator_id') or None
        assigned_to_id = request.POST.get('assigned_to_id') or None

        if id_pedido:
            # Atualização na BD
            atualizar_pedido(id_pedido, title, description, status, id_tipo_pedido, creator_id, assigned_to_id)
        else:
            # Criação na BD
            id_pedido = criar_pedido(title, description, status, creator_id, id_tipo_pedido, assigned_to_id)
        
        # Gestão de arquivos
        if request.FILES.get('pedido_ficheiro'):
            ficheiro = request.FILES['pedido_ficheiro']
            file_name = ficheiro.name
            file_path = f"/media/pedidos/{file_name}"
            adicionar_ficheiro_pedido(file_name, file_path, id_pedido)

        return redirect('lista_pedidos')

    contexto = {
        'pedido': pedido_existente,
        'tipos_pedido': tipos_reais,
        'utilizadores': utilizadores_reais, # <-- Enviado para o HTML
        'ficheiros': ficheiros_anexados
    }
    return render(request, 'utilizadores/requestform.html', contexto)

def apagar_pedido(request, id_pedido):
    eliminar_pedido(id_pedido)
    return redirect('lista_pedidos')