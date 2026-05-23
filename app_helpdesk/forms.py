from django import forms
from .models import Cliente

ASSUNTO_CHOICES = [
    ('NOSSOS APLICATIVOS', 'Nossos Aplicativos'),
    ('DÚVIDAS FINANCEIRAS', 'Dúvidas Financeiras'),
    ('SUPORTE TÉCNICO', 'Suporte Técnico'),
    ('RECLAMAÇÕES', 'Reclamações'),
    ('OUTRAS INFORMAÇÕES', 'Outras Informações')
]

PRIORIDADE_CHOICES = [
    ('BAIXA', 'Baixa'),
    ('MÉDIA', 'Média'),
    ('ALTA', 'Alta'),
    ('A DEFINIR', 'A Definir')
]

class ClienteForm(forms.ModelForm):
    assunto = forms.ChoiceField(choices=ASSUNTO_CHOICES, label='Assunto')
    descricao = forms.CharField(widget=forms.Textarea, label='Descrição', max_length=300)

    class Meta:
        model = Cliente
        fields = ['nomecliente', 'cpf_cnpj', 'email_cliente', 'telefone_cliente', 'assunto', 'descricao']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Usuário')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

class SolicitacaoForm(forms.Form):
    assunto = forms.ChoiceField(choices=ASSUNTO_CHOICES, label='Assunto')
    prioridade = forms.ChoiceField(choices=PRIORIDADE_CHOICES, label='Prioridade')

class RespostaForm(forms.Form):
    resposta_usuario = forms.CharField(widget=forms.Textarea, required=False, label='Resposta')
