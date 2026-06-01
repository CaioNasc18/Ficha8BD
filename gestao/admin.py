from django.contrib import admin
from .models import (
	TiposUtilizadores, Empresas, Utilizadores, Logs,
	Duvidas, MensagensDuvida, TiposPedido, Pedido,
	EstadosPedidos, Ficheiros
)


@admin.register(TiposUtilizadores)
class TiposUtilizadoresAdmin(admin.ModelAdmin):
	list_display = ('id', 'designacao')


@admin.register(Empresas)
class EmpresasAdmin(admin.ModelAdmin):
	list_display = ('id', 'nome')


@admin.register(Utilizadores)
class UtilizadoresAdmin(admin.ModelAdmin):
	list_display = ('id', 'nome', 'email', 'telefone', 'ativo')
	search_fields = ('nome', 'email')


@admin.register(Logs)
class LogsAdmin(admin.ModelAdmin):
	list_display = ('id', 'utilizador', 'acao', 'data_hora')


@admin.register(Duvidas)
class DuvidasAdmin(admin.ModelAdmin):
	list_display = ('id', 'assunto', 'estado', 'data_criacao')


@admin.register(MensagensDuvida)
class MensagensDuvidaAdmin(admin.ModelAdmin):
	list_display = ('id', 'duvida', 'utilizador', 'data_envio')


@admin.register(TiposPedido)
class TiposPedidoAdmin(admin.ModelAdmin):
	list_display = ('id', 'nome')


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
	list_display = ('id', 'assunto', 'tipo', 'criador', 'estado', 'data_abertura')


@admin.register(EstadosPedidos)
class EstadosPedidosAdmin(admin.ModelAdmin):
	list_display = ('id', 'pedido', 'estado', 'data')


@admin.register(Ficheiros)
class FicheirosAdmin(admin.ModelAdmin):
	list_display = ('id', 'pedido', 'nome', 'data_upload')
