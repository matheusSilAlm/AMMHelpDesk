import os
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from app_helpdesk.models import Cliente, Solicitacao, Solicitacaostatus, models
from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
from bs4 import BeautifulSoup
from django.templatetags.static import static
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from django.db.models import Q
import base64
import re
import logging
logger = logging.getLogger('app_helpdesk')
from app_helpdesk.forms import ClienteForm, LoginForm, RespostaForm

# Usuário faz login na pagina.
def login_user(request):
    return render(request, 'login.html')

#Usuário faz logout na pagina.
def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            usuario = authenticate(username=username, password=password)
            if usuario is not None:
                login(request, usuario)
                return redirect('/')
            else:
                messages.error(request, "Usuário ou senha inválidos")
        else:
            messages.error(request, "Dados inválidos no formulário.")
    return redirect('/')

@login_required(login_url='/login/')
def solicit_pages(request):
    usuario = request.user
    statuscliente = request.GET.get('status')
    prioridadecliente = request.GET.get('prioridade')
    arr_cliente = list(Cliente.objects.order_by('-idcliente').prefetch_related(
        'solicitacao_set__solicitacaostatus_set'
    ))

    for cliente in arr_cliente:
        solicitacao = cliente.solicitacao_set.first()
        if solicitacao:
            cliente.prioridade = solicitacao.prioridade
            status_obj = solicitacao.solicitacaostatus_set.first()
            cliente.status = status_obj.idstatus if status_obj else 'ABERTO'
        else:
            cliente.prioridade = 'A DEFINIR'
            cliente.status = 'ABERTO'
    
    cliente = {
        'clientes': arr_cliente
    }

    paginator = Paginator(arr_cliente, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'listpage.html', {'page_obj':page_obj})  

def cliente_page(request):
    return render(request, 'FormsHD.html')

def cliente_novo(request):
    novo_cliente = Cliente()
    novo_cliente.nomecliente = request.POST.get('nomecliente')
    novo_cliente.assunto = request.POST.get('assunto')

    cliente = {
        'cliente': Cliente.objects.all()
    }
    return render(request, '/', cliente)

@login_required(login_url='/login/')
def atender_cliente(request):
    idcliente = request.GET.get('id')
    dados = {}
    if idcliente:
        dados['cliente'] = Cliente.objects.filter(idcliente=idcliente).first()
        if not dados['cliente']:
            return HttpResponse("Chamado não encontrado.", status=404)

    return render(request, 'pagecliente.html',dados)

@login_required(login_url='/login/')
def update_cliente(request, idcliente):
    statuscliente = request.GET.get('status')
    prioridadecliente = request.GET.get('prioridade')
    faq_enviar = request.GET.get('faq_enviado')
    resposta_usuario = request.POST.get('resposta_usuario')
    
    if statuscliente:
        v_solicitacao = Solicitacao.objects.filter(idcliente=idcliente).first()
        if not v_solicitacao: return redirect('/')
        v_solicitacaostatus = Solicitacaostatus.objects.filter(idsolicitacao=v_solicitacao.idsolicitacao).first()
        if not v_solicitacaostatus: return redirect('/')
        v_solicitacaostatus.idstatus = statuscliente
        v_solicitacaostatus.save()
        return redirect('/')
    
    elif prioridadecliente:
        v_solicitacao = Solicitacao.objects.filter(idcliente=idcliente).first()
        if not v_solicitacao: return redirect('/')
        v_solicitacao.prioridade = prioridadecliente
        v_solicitacao.save()
        return redirect('/')
    
    elif faq_enviar:
        v_faq_enviar = Cliente.objects.filter(idcliente=idcliente).first()
        if not v_faq_enviar: return redirect('/')
        v_faq_enviar.faq_enviar = faq_enviar
        v_faq_enviar.save()

        return redirect('/')
    
    
    elif request.method == 'POST':
        cliente = Cliente.objects.filter(idcliente=idcliente).first()
        if not cliente: return redirect('/')
        resposta = request.POST.get('resposta_usuario_' + str(idcliente))
        form = RespostaForm({'resposta_usuario': resposta})
        
        if form.is_valid():
            resposta_usuario = form.cleaned_data.get('resposta_usuario') or ''
            cliente.resposta_usuario = resposta_usuario
        
            pattern = r'<img src="([^"]+)" />'
            matches = re.findall(pattern, resposta_usuario)
    
            image_email = []
        for idx, src in enumerate(matches):
            resp = resposta_usuario.split('"')
            data = resp[1]    
            image_id = f'cid:image_teste{idx + 1}'
            
            resposta_usuario = resposta_usuario.replace(src, image_id)

            resp = src.split(",")

            format_file = resp[0].split(";")[0].split('/')[1]

            image = {
                'binario': resp[1],
                'format': format_file,
                'file_name':f'image_teste{idx + 1}'
            }
    
            image_email.append(image)

        subject = f'Resposta ao seu chamado: {cliente.assunto}' 
        from_email = 'teushiftz@gmail.com'  
        to_email = cliente.email_cliente  

        context = {
            'cliente': cliente,
            'resposta_usuario': resposta_usuario,
        }

        html_message = render_to_string('pageclienteX.html', context)
        html_message = html_message.replace('src="logo_image"', f'src="cid:logo_image"')
        text_message = strip_tags(html_message)

        email = EmailMultiAlternatives(subject, text_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")

        image_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'amm-navbar-fnt.png')
        with open(image_path, 'rb') as f:
            image_data = f.read()
        image = MIMEImage(image_data, _subtype='png')
        image.add_header('Content-ID', '<logo_image>')
        image.add_header('Content-Disposition', 'inline', filename='amm-navbar-fnt.png')
        email.attach(image)

        for idx, src in enumerate(image_email):
            image_data = base64.b64decode(src['binario'])

            image_path = os.path.join(settings.BASE_DIR, 'static', 'img', f'{src["file_name"]}.{src["format"]}')
            img_file = open(image_path, 'wb')
            img_file.write(image_data)
            img_file.close()

            with open(image_path, 'rb') as f:
                image_data = f.read()
            image = MIMEImage(image_data)
            image.add_header('Content-ID', f'<{src["file_name"]}>')
            image.add_header('Content-Disposition', 'inline', filename=f'{src["file_name"]}.{src["format"]}')
            email.attach(image)
  
        
        anexo = request.FILES.get('anexo')
        if anexo:
            email.attach(anexo.name, anexo.read(), anexo.content_type)

        if os.path.exists(image_path):
            os.remove(image_path)

        try:
            email.send()
        except Exception as e:
            logger.error("Falha ao enviar email para %s: %s", cliente.email_cliente, e)

        cliente.save()
        # return render(request, 'teste.html', {'resposta_usuario':''.join(image_email)})
        return redirect('/')
        
        else:
            messages.error(request, "Erro no formulário de resposta.")
            return redirect('/')

    return redirect(request.path_info)


def cliente_page_submit(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            nomecliente = form.cleaned_data['nomecliente']
            cpf_cnpj = form.cleaned_data['cpf_cnpj']
            email_cliente = form.cleaned_data['email_cliente']
            telefone_cliente = form.cleaned_data['telefone_cliente']
            descricao = form.cleaned_data['descricao']
            assunto = form.cleaned_data['assunto']

            with transaction.atomic():
                cliente = Cliente.objects.create(
                    nomecliente=nomecliente,
                    cpf_cnpj=cpf_cnpj,
                    email_cliente=email_cliente,
                    telefone_cliente=telefone_cliente,
                    descricao=descricao,
                    assunto=assunto
                )

                solicitacao = Solicitacao.objects.create(
                    assunto=assunto,
                    idcliente=cliente,
                    prioridade='A DEFINIR'
                )
                solicitacaostatus = Solicitacaostatus.objects.create(
                    idstatus='ABERTO',
                    idsolicitacao=solicitacao
                )
        else:
            messages.error(request, "Por favor, corrija os erros no formulário.")
            
    return  render(request, 'formshd.html')


def faq_amm(request):
    query = request.GET.get('q')  # Obtém o parâmetro de pesquisa da URL

    if query:
        # Realize a pesquisa no banco de dados usando a sua lógica
        clientes = Cliente.objects.filter(
            Q(assunto__icontains=query) | Q(descricao__icontains=query)
        )
    else:
        # Se nenhum parâmetro de pesquisa for fornecido, retorne todos os clientes
        clientes = Cliente.objects.all()

    dados = {'clientes': clientes, 'query': query}
    return render(request, 'FAQ.html', dados)