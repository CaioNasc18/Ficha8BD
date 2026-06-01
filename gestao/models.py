from django.db import models


# Types of users (tipos_utilizadores)
class TiposUtilizadores(models.Model):
	designacao = models.CharField(max_length=120)

	def __str__(self):
		return self.designacao


class Empresas(models.Model):
	nome = models.CharField(max_length=200)

	def __str__(self):
		return self.nome


# Utilizadores table (separate from django auth for now)
class Utilizadores(models.Model):
	tipo = models.ForeignKey(TiposUtilizadores, on_delete=models.SET_NULL, null=True)
	empresa = models.ForeignKey(Empresas, on_delete=models.SET_NULL, null=True, blank=True)
	email = models.EmailField(unique=True)
	password_hash = models.CharField(max_length=255)
	nome = models.CharField(max_length=200)
	telefone = models.CharField(max_length=50, blank=True)
	ativo = models.BooleanField(default=True)
	data_criacao = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.nome


class Logs(models.Model):
	utilizador = models.ForeignKey(Utilizadores, on_delete=models.SET_NULL, null=True, blank=True)
	acao = models.CharField(max_length=200)
	entidade = models.CharField(max_length=100)
	detalhes = models.TextField(blank=True)
	data_hora = models.DateTimeField(auto_now_add=True)
	ip = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return f"{self.id} - {self.acao}"


class Duvidas(models.Model):
	criador = models.ForeignKey(Utilizadores, on_delete=models.SET_NULL, null=True, related_name='duvidas_criadas')
	responsavel = models.ForeignKey(Utilizadores, on_delete=models.SET_NULL, null=True, blank=True, related_name='duvidas_responsavel')
	assunto = models.CharField(max_length=200)
	estado = models.CharField(max_length=80, blank=True)
	data_criacao = models.DateTimeField(auto_now_add=True)
	data_fecho = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"{self.pk} - {self.assunto}"


class MensagensDuvida(models.Model):
	duvida = models.ForeignKey(Duvidas, on_delete=models.CASCADE, related_name='mensagens')
	utilizador = models.ForeignKey(Utilizadores, on_delete=models.SET_NULL, null=True)
	mensagem = models.TextField()
	data_envio = models.DateTimeField(auto_now_add=True)
	lida = models.BooleanField(default=False)

	def __str__(self):
		return f"Mensagem {self.pk} - Duvida {self.duvida_id}"


class TiposPedido(models.Model):
	nome = models.CharField(max_length=120)

	def __str__(self):
		return self.nome


class Pedido(models.Model):
	tipo = models.ForeignKey(TiposPedido, on_delete=models.SET_NULL, null=True, blank=True)
	criador = models.ForeignKey(Utilizadores, on_delete=models.SET_NULL, null=True, related_name='pedidos_criados')
	responsavel = models.ForeignKey(Utilizadores, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos_responsaveis')
	assunto = models.CharField(max_length=200)
	descricao = models.TextField(blank=True)
	estado = models.CharField(max_length=80, blank=True)
	data_abertura = models.DateTimeField(auto_now_add=True)
	data_fecho = models.DateTimeField(null=True, blank=True)

	def __str__(self):
		return f"{self.pk} - {self.assunto}"


class EstadosPedidos(models.Model):
	pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='estados')
	estado = models.CharField(max_length=120)
	observacao = models.TextField(blank=True)
	data = models.DateTimeField(auto_now_add=True)
	utilizador = models.ForeignKey(Utilizadores, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return f"{self.pedido_id} - {self.estado}"


class Ficheiros(models.Model):
	pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='ficheiros')
	nome = models.CharField(max_length=255, blank=True)
	ficheiro = models.FileField(upload_to='ficheiros/', null=True, blank=True)
	data_upload = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.nome or (self.ficheiro.name if self.ficheiro else str(self.pk))
