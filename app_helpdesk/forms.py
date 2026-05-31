import re
from django import forms
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags
from .models import Cliente


ASSUNTO_CHOICES = [
    ('', 'Selecione um assunto'),
    ('NOSSOS APLICATIVOS', 'Nossos Aplicativos'),
    ('DÚVIDAS FINANCEIRAS', 'Dúvidas Financeiras'),
    ('SUPORTE TÉCNICO', 'Suporte Técnico'),
    ('RECLAMAÇÕES', 'Reclamações'),
    ('OUTRAS INFORMAÇÕES', 'Outras Informações'),
]

PRIORIDADE_CHOICES = [
    ('BAIXA', 'Baixa'),
    ('MÉDIA', 'Média'),
    ('ALTA', 'Alta'),
    ('A DEFINIR', 'A Definir'),
]


def validate_cpf_cnpj(value):
    """Valida CPF (11 dígitos) ou CNPJ (14 dígitos)."""
    digits_only = re.sub(r'\D', '', value)
    if len(digits_only) not in (11, 14):
        raise ValidationError(
            'CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos. '
            f'Recebido: {len(digits_only)} dígitos.',
            code='invalid_cpf_cnpj',
        )


def validate_telefone_br(value):
    """Valida telefone brasileiro (8-20 caracteres, aceita +, dígitos, espaços, hífens, parênteses)."""
    cleaned = re.sub(r'[\s\-\(\)\+]', '', value)
    if not cleaned.isdigit():
        raise ValidationError(
            'Telefone deve conter apenas dígitos, espaços, hífens e parênteses.',
            code='invalid_phone',
        )
    if len(cleaned) < 8 or len(cleaned) > 15:
        raise ValidationError(
            'Telefone deve ter entre 8 e 15 dígitos.',
            code='invalid_phone_length',
        )


class ClienteForm(forms.ModelForm):
    """Formulário de abertura de chamado pelo cliente."""

    nomecliente = forms.CharField(
        max_length=80,
        label='Nome Completo',
        widget=forms.TextInput(attrs={'placeholder': 'Seu nome completo'}),
    )
    cpf_cnpj = forms.CharField(
        max_length=20,
        label='CPF ou CNPJ',
        validators=[validate_cpf_cnpj],
        widget=forms.TextInput(attrs={'placeholder': 'Somente números'}),
    )
    email_cliente = forms.EmailField(
        max_length=80,
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder': 'exemplo@empresa.com'}),
    )
    telefone_cliente = forms.CharField(
        max_length=20,
        label='Telefone / WhatsApp',
        validators=[validate_telefone_br],
        widget=forms.TextInput(attrs={'placeholder': '(00) 00000-0000'}),
    )
    assunto = forms.ChoiceField(
        choices=ASSUNTO_CHOICES,
        label='Assunto',
    )
    descricao = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        label='Descrição',
        max_length=300,
    )

    class Meta:
        model = Cliente
        fields = [
            'nomecliente',
            'cpf_cnpj',
            'email_cliente',
            'telefone_cliente',
            'assunto',
            'descricao',
        ]

    def clean_assunto(self):
        """Garante que o assunto é uma opção válida e não o placeholder vazio."""
        assunto = self.cleaned_data.get('assunto')
        if not assunto:
            raise ValidationError('Por favor, selecione um assunto válido.', code='required')
        return assunto


class LoginForm(forms.Form):
    """Formulário de autenticação de usuário."""

    username = forms.CharField(
        max_length=150,
        label='Usuário',
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu usuário', 'autocomplete': 'username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha', 'autocomplete': 'current-password'}),
        label='Senha',
    )


class SolicitacaoForm(forms.Form):
    """Formulário de criação de solicitação."""

    assunto = forms.ChoiceField(choices=ASSUNTO_CHOICES, label='Assunto')
    prioridade = forms.ChoiceField(choices=PRIORIDADE_CHOICES, label='Prioridade')


class RespostaForm(forms.Form):
    """Formulário de resposta ao chamado (preenchido por staff)."""

    resposta_usuario = forms.CharField(
        widget=forms.Textarea,
        required=False,
        label='Resposta',
        max_length=50000,
    )

    def clean_resposta_usuario(self):
        """Preserva HTML seguro do CKEditor mas remove tags potencialmente perigosas."""
        value = self.cleaned_data.get('resposta_usuario', '')
        # Allow the CKEditor HTML to pass through - it's staff-only input
        # but strip any script tags as a defense-in-depth measure
        value = re.sub(r'<script[^>]*>.*?</script>', '', value, flags=re.DOTALL | re.IGNORECASE)
        value = re.sub(r'<iframe[^>]*>.*?</iframe>', '', value, flags=re.DOTALL | re.IGNORECASE)
        return value
