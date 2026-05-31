import os
import re
import base64
import logging
from functools import partial

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from email.mime.image import MIMEImage

from app_helpdesk.forms import ClienteForm, LoginForm, RespostaForm
from app_helpdesk.models import Cliente, Solicitacao, Solicitacaostatus

logger = logging.getLogger('app_helpdesk')


def login_user(request):
    """Render the login page."""
    return render(request, 'login.html')


def logout_user(request):
    """Log out the current user and redirect to root."""
    logout(request)
    return redirect('/')


def submit_login(request):
    """Process login form submission."""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usuario = authenticate(request, username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                logger.info("Login bem-sucedido para o usuário: %s", username)
                return redirect('/')
            else:
                logger.warning("Tentativa de login falhou para o usuário: %s", username)
                messages.error(request, 'Usuário ou senha inválidos')
        else:
            messages.error(request, 'Dados inválidos no formulário.')
    return redirect('/login/')


@login_required(login_url='/login/')
def solicit_pages(request):
    """List all support tickets with status and priority from related models."""
    arr_cliente = list(
        Cliente.objects.order_by('-idcliente').prefetch_related(
            'solicitacao_set__solicitacaostatus_set'
        )
    )

    for cliente in arr_cliente:
        solicitacao = cliente.solicitacao_set.first()
        if solicitacao:
            cliente.prioridade = solicitacao.prioridade
            status_obj = solicitacao.solicitacaostatus_set.first()
            cliente.status = status_obj.idstatus if status_obj else 'ABERTO'
        else:
            cliente.prioridade = 'A DEFINIR'
            cliente.status = 'ABERTO'

    paginator = Paginator(arr_cliente, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listpage.html', {'page_obj': page_obj})


def cliente_page(request):
    """Render the public ticket submission form."""
    return render(request, 'FormsHD.html')


def cliente_novo(request):
    """Stub view — preserved for backward-compat URL routing."""
    return redirect('/home/')


@login_required(login_url='/login/')
def atender_cliente(request):
    """Show ticket detail page for staff to respond."""
    idcliente = request.GET.get('id')
    dados = {}
    if idcliente:
        dados['cliente'] = Cliente.objects.filter(idcliente=idcliente).first()
        if not dados['cliente']:
            return HttpResponse('Chamado não encontrado.', status=404)
    return render(request, 'pagecliente.html', dados)


def _send_response_email(cliente_id, resposta_usuario, anexo_name=None, anexo_data=None, anexo_type=None):
    """Send the response email to the client. Called via transaction.on_commit."""
    try:
        cliente = Cliente.objects.filter(idcliente=cliente_id).first()
        if not cliente:
            logger.error("Email não enviado: cliente %s não encontrado após commit.", cliente_id)
            return

        subject = f'Resposta ao seu chamado: {cliente.assunto}'
        from_email = settings.EMAIL_HOST_USER
        to_email = cliente.email_cliente

        context = {
            'cliente': cliente,
            'resposta_usuario': resposta_usuario,
        }

        html_message = render_to_string('pageclienteX.html', context)
        html_message = html_message.replace('src="logo_image"', 'src="cid:logo_image"')
        text_message = strip_tags(html_message)

        email = EmailMultiAlternatives(subject, text_message, from_email, [to_email])
        email.attach_alternative(html_message, 'text/html')

        # Attach company logo
        logo_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'amm-navbar-fnt.png')
        if os.path.exists(logo_path):
            with open(logo_path, 'rb') as f:
                logo_data = f.read()
            logo_img = MIMEImage(logo_data, _subtype='png')
            logo_img.add_header('Content-ID', '<logo_image>')
            logo_img.add_header('Content-Disposition', 'inline', filename='amm-navbar-fnt.png')
            email.attach(logo_img)

        # Attach file if provided
        if anexo_name and anexo_data:
            email.attach(anexo_name, anexo_data, anexo_type)

        email.send()
        logger.info("Email de resposta enviado para %s (chamado %s)", to_email, cliente_id)

    except Exception as exc:
        logger.error(
            "Falha ao enviar email para cliente %s: %s",
            cliente_id,
            exc,
            exc_info=True,
        )


@login_required(login_url='/login/')
def update_cliente(request, idcliente):
    """Update ticket status, priority, FAQ flag, or save a staff response with email."""
    statuscliente = request.GET.get('status')
    prioridadecliente = request.GET.get('prioridade')
    faq_enviar = request.GET.get('faq_enviado')

    if statuscliente:
        v_solicitacao = Solicitacao.objects.filter(idcliente=idcliente).first()
        if not v_solicitacao:
            return redirect('/')
        v_solicitacaostatus = Solicitacaostatus.objects.filter(
            idsolicitacao=v_solicitacao.idsolicitacao
        ).first()
        if not v_solicitacaostatus:
            return redirect('/')
        v_solicitacaostatus.idstatus = statuscliente
        v_solicitacaostatus.save()
        logger.info("Status do chamado %s atualizado para: %s", idcliente, statuscliente)
        return redirect('/')

    elif prioridadecliente:
        v_solicitacao = Solicitacao.objects.filter(idcliente=idcliente).first()
        if not v_solicitacao:
            return redirect('/')
        v_solicitacao.prioridade = prioridadecliente
        v_solicitacao.save()
        logger.info("Prioridade do chamado %s atualizada para: %s", idcliente, prioridadecliente)
        return redirect('/')

    elif faq_enviar:
        v_cliente = Cliente.objects.filter(idcliente=idcliente).first()
        if not v_cliente:
            return redirect('/')
        v_cliente.faq_enviar = faq_enviar
        v_cliente.save()
        logger.info("FAQ marcado para envio no chamado %s", idcliente)
        return redirect('/')

    elif request.method == 'POST':
        cliente = Cliente.objects.filter(idcliente=idcliente).first()
        if not cliente:
            return redirect('/')

        resposta = request.POST.get(f'resposta_usuario_{idcliente}')
        form = RespostaForm({'resposta_usuario': resposta})

        if not form.is_valid():
            messages.error(request, 'Erro no formulário de resposta.')
            return redirect('/')

        resposta_usuario = form.cleaned_data.get('resposta_usuario') or ''

        # Process inline base64 images embedded by CKEditor — replace with cid: references
        pattern = r'<img src="(data:[^;]+;base64,[^"]+)" />'
        matches = re.findall(pattern, resposta_usuario)
        image_refs = []

        for idx, src in enumerate(matches):
            cid_name = f'inline_image_{idcliente}_{idx + 1}'
            image_id = f'cid:{cid_name}'
            resposta_usuario = resposta_usuario.replace(src, image_id)

            parts = src.split(',')
            if len(parts) < 2:
                continue
            format_part = parts[0]  # e.g. data:image/png;base64
            try:
                fmt = format_part.split(';')[0].split('/')[1]
            except IndexError:
                fmt = 'png'

            image_refs.append({
                'binario': parts[1],
                'format': fmt,
                'cid_name': cid_name,
            })

        # Read file attachment before transaction commit (request is not available in callback)
        anexo = request.FILES.get('anexo')
        anexo_name = anexo.name if anexo else None
        anexo_data = anexo.read() if anexo else None
        anexo_type = anexo.content_type if anexo else None

        with transaction.atomic():
            cliente.resposta_usuario = resposta_usuario
            cliente.save()
            logger.info("Resposta salva no chamado %s", idcliente)

            # Schedule email to send AFTER the DB transaction commits successfully
            transaction.on_commit(
                partial(
                    _send_response_email,
                    cliente.idcliente,
                    resposta_usuario,
                    anexo_name,
                    anexo_data,
                    anexo_type,
                )
            )

        return redirect('/')

    return redirect(request.path_info)


def cliente_page_submit(request):
    """Process public ticket submission form."""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                cliente = Cliente.objects.create(
                    nomecliente=form.cleaned_data['nomecliente'],
                    cpf_cnpj=form.cleaned_data['cpf_cnpj'],
                    email_cliente=form.cleaned_data['email_cliente'],
                    telefone_cliente=form.cleaned_data['telefone_cliente'],
                    descricao=form.cleaned_data['descricao'],
                    assunto=form.cleaned_data['assunto'],
                )
                solicitacao = Solicitacao.objects.create(
                    assunto=form.cleaned_data['assunto'],
                    idcliente=cliente,
                    prioridade='A DEFINIR',
                )
                Solicitacaostatus.objects.create(
                    idstatus='ABERTO',
                    idsolicitacao=solicitacao,
                )
            logger.info("Novo chamado criado: ID %s — %s", cliente.idcliente, cliente.assunto)
            messages.success(request, 'Chamado aberto com sucesso! Entraremos em contato em breve.')
        else:
            logger.warning("Formulário de chamado inválido: %s", form.errors)
            messages.error(request, 'Por favor, corrija os erros no formulário.')

    return render(request, 'FormsHD.html')


def faq_amm(request):
    """Public FAQ page with optional keyword search."""
    query = request.GET.get('q')

    if query:
        clientes = Cliente.objects.filter(
            Q(assunto__icontains=query) | Q(descricao__icontains=query),
            faq_enviar__isnull=False,
        )
    else:
        clientes = Cliente.objects.filter(faq_enviar__isnull=False)

    dados = {'clientes': clientes, 'query': query}
    return render(request, 'FAQ.html', dados)