from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse

from .models import Pedido, Utilizadores, Duvidas, MensagensDuvida, Ficheiros
from .forms import PedidoForm, UtilizadorForm, DuvidaForm, MensagemDuvidaForm, FicheiroForm


def index(request):
    return render(request, 'index.html')


def list_pedidos_exame(request):
    pedidos = Pedido.objects.select_related('tipo', 'criador', 'responsavel').all()
    return render(request, 'list_pedidos_exame.html', {'pedidos_exame': pedidos})


def register_pedido_exame(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            pedido = form.save(commit=False)
            if request.user.is_authenticated:
                criador = Utilizadores.objects.filter(email=getattr(request.user, 'email', None)).first()
                if criador:
                    pedido.criador = criador
            pedido.save()
            return redirect('list_pedidos_exame')
    else:
        form = PedidoForm()
    return render(request, 'register_form.html', {'form': form, 'title': 'Novo Pedido de Exame'})


def edit_pedido_exame(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('list_pedidos_exame')
    else:
        form = PedidoForm(instance=pedido)
    return render(request, 'register_form.html', {'form': form, 'title': 'Editar Pedido'})


def delete_pedido_exame(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        pedido.delete()
        return redirect('list_pedidos_exame')
    return render(request, 'confirm_delete.html', {'object': pedido, 'title': 'Eliminar Pedido', 'cancel_url': 'list_pedidos_exame'})


# Placeholder views for templates navigation (will be implemented later)
def list_doentes(request):
    return render(request, 'list_doentes.html', {'doentes': []})


def list_consultas(request):
    return render(request, 'list_consultas.html', {'consultas': []})


def register_doente(request):
    return render(request, 'register_form.html', {'form': None, 'title': 'Registar Doente'})


def register_consulta(request):
    return render(request, 'register_form.html', {'form': None, 'title': 'Nova Consulta'})


# Utilizadores CRUD
def list_utilizadores(request):
    utilizadores = Utilizadores.objects.select_related('tipo', 'empresa').all()
    return render(request, 'list_utilizadores.html', {'utilizadores': utilizadores})


def register_utilizador(request):
    if request.method == 'POST':
        form = UtilizadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_utilizadores')
    else:
        form = UtilizadorForm()
    return render(request, 'register_form.html', {'form': form, 'title': 'Registar Utilizador'})


def edit_utilizador(request, pk):
    utilizador = get_object_or_404(Utilizadores, pk=pk)
    if request.method == 'POST':
        form = UtilizadorForm(request.POST, instance=utilizador)
        if form.is_valid():
            form.save()
            return redirect('list_utilizadores')
    else:
        form = UtilizadorForm(instance=utilizador)
    return render(request, 'register_form.html', {'form': form, 'title': 'Editar Utilizador'})


def delete_utilizador(request, pk):
    utilizador = get_object_or_404(Utilizadores, pk=pk)
    if request.method == 'POST':
        utilizador.delete()
        return redirect('list_utilizadores')
    return render(request, 'confirm_delete.html', {'object': utilizador, 'title': 'Eliminar Utilizador', 'cancel_url': 'list_utilizadores'})


# Duvidas CRUD + detail with messages
def list_duvidas(request):
    duvidas = Duvidas.objects.select_related('criador', 'responsavel').all()
    return render(request, 'list_duvidas.html', {'duvidas': duvidas})


def register_duvida(request):
    if request.method == 'POST':
        form = DuvidaForm(request.POST)
        if form.is_valid():
            duvida = form.save(commit=False)
            if request.user.is_authenticated:
                criador = Utilizadores.objects.filter(email=getattr(request.user, 'email', None)).first()
                if criador:
                    duvida.criador = criador
            duvida.save()
            return redirect('list_duvidas')
    else:
        form = DuvidaForm()
    return render(request, 'register_form.html', {'form': form, 'title': 'Nova Dúvida'})


def detail_duvida(request, pk):
    duvida = get_object_or_404(Duvidas, pk=pk)
    mensagens = duvida.mensagens.select_related('utilizador').all()
    if request.method == 'POST':
        form = MensagemDuvidaForm(request.POST)
        if form.is_valid():
            mensagem = form.save(commit=False)
            mensagem.duvida = duvida
            if request.user.is_authenticated:
                utiliz = Utilizadores.objects.filter(email=getattr(request.user, 'email', None)).first()
                if utiliz:
                    mensagem.utilizador = utiliz
            mensagem.save()
            return redirect('detail_duvida', pk=duvida.pk)
    else:
        form = MensagemDuvidaForm()
    return render(request, 'detail_duvida.html', {'duvida': duvida, 'mensagens': mensagens, 'form': form})


def edit_duvida(request, pk):
    duvida = get_object_or_404(Duvidas, pk=pk)
    if request.method == 'POST':
        form = DuvidaForm(request.POST, instance=duvida)
        if form.is_valid():
            form.save()
            return redirect('list_duvidas')
    else:
        form = DuvidaForm(instance=duvida)
    return render(request, 'register_form.html', {'form': form, 'title': 'Editar Dúvida'})


def delete_duvida(request, pk):
    duvida = get_object_or_404(Duvidas, pk=pk)
    if request.method == 'POST':
        duvida.delete()
        return redirect('list_duvidas')
    return render(request, 'confirm_delete.html', {'object': duvida, 'title': 'Eliminar Dúvida', 'cancel_url': 'list_duvidas'})


# File upload for Pedido
def upload_ficheiro(request, pk):
    pedido = get_object_or_404(Pedido, pk=pk)
    if request.method == 'POST':
        form = FicheiroForm(request.POST, request.FILES)
        if form.is_valid():
            ficheiro = form.save(commit=False)
            ficheiro.pedido = pedido
            ficheiro.save()
            return redirect('list_pedidos_exame')
    else:
        form = FicheiroForm()
    return render(request, 'upload_ficheiro.html', {'pedido': pedido, 'form': form})

    