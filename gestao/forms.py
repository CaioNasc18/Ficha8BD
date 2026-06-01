from django import forms
from .models import Pedido


class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['tipo', 'assunto', 'descricao', 'responsavel']
        widgets = {
            'descricao': forms.Textarea(attrs={'rows':4}),
        }


from .models import Utilizadores, Duvidas, MensagensDuvida


class UtilizadorForm(forms.ModelForm):
    class Meta:
        model = Utilizadores
        fields = ['tipo', 'empresa', 'email', 'password_hash', 'nome', 'telefone', 'ativo']
        widgets = {
            'password_hash': forms.PasswordInput(render_value=False),
        }


class DuvidaForm(forms.ModelForm):
    class Meta:
        model = Duvidas
        fields = ['assunto', 'responsavel', 'estado']


class MensagemDuvidaForm(forms.ModelForm):
    class Meta:
        model = MensagensDuvida
        fields = ['mensagem']
        widgets = {
            'mensagem': forms.Textarea(attrs={'rows':3}),
        }


from .models import Ficheiros


class FicheiroForm(forms.ModelForm):
    class Meta:
        model = Ficheiros
        fields = ['nome', 'ficheiro']
