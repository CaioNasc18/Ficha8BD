from django.shortcuts import render, redirect
from django.http import Http404
# Corrigido aqui para 'obtener_utilizador_por_id'
from .basedados import (
    listar_todos_utilizadores, obtener_utilizador_por_id, criar_utilizador,
    atualizar_utilizador, eliminar_utilizador, listar_tipos_utilizador, listar_empresas
)


# 1. Página de Listagem Geral
def lista_utilizadores(request):
    utilizadores = listar_todos_utilizadores()
    return render(request, 'utilizadores/lista.html', {'utilizadores': utilizadores})

# 2. Página Única de Formulário (Gere Criação e Edição)
def gerir_utilizador(request, id_utilizador=None):
    utilizador = None
    
    if id_utilizador:
        # CORRIGIDO: Agora usa 'obtener_utilizador_por_id' com 'n'
        utilizador = obtener_utilizador_por_id(id_utilizador)
        if not utilizador:
            raise Http404("Utilizador não encontrado.")
        # Segurança extra para o HTML ler o ID independentemente de maiúsculas/minúsculas
        utilizador['id_Utilizador'] = utilizador.get('id_Utilizador') or utilizador.get('id_utilizador')

    if request.method == 'POST':
        email = request.POST.get('email')
        name = request.POST.get('name')
        telephone = request.POST.get('telephone')
        active = 1 if request.POST.get('active') == 'on' else 0
        id_tipo = request.POST.get('id_tipo')
        id_empresa = request.POST.get('id_empresa')

        if id_utilizador:
            atualizar_utilizador(id_utilizador, email, name, telephone, active, id_tipo, id_empresa)
        else:
            password = request.POST.get('password')
            criar_utilizador(email, password, name, telephone, active, id_tipo, id_empresa)
            
        return redirect('lista_utilizadores')

    # Carrega os dados auxiliares das tabelas estrangeiras
    tipos = listar_tipos_utilizador()
    empresas = listar_empresas()

    return render(request, 'utilizadores/formulario.html', {
        'utilizador': utilizador,
        'tipos': tipos,
        'empresas': empresas
    })


# 3. Rota de Eliminação Direta
def apagar_utilizador(request, id_utilizador):
    eliminar_utilizador(id_utilizador)
    return redirect('lista_utilizadores')
