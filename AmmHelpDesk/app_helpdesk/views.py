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


# Usuário faz login na pagina.
def login_user(request):
    return render(request, 'login.html')

#Usuário faz logout na pagina.
def logout_user(request):
    logout(request)
    return redirect('/')

def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        else:
            messages.error(request, "Usuário ou senha inválidos")
    return redirect('/')

@login_required(login_url='/login/')
def solicit_pages(request):
    usuario = request.user
    statuscliente = request.GET.get('status')
    prioridadecliente = request.GET.get('prioridade')
    arr_cliente = Cliente.objects.all() and Cliente.objects.order_by('-idcliente')
    
    for index, cliente in enumerate(arr_cliente, start=0):
        v_solicitacao = Solicitacao.objects.get(idcliente=arr_cliente[index].idcliente)
        v_solicitacaostatus = Solicitacaostatus.objects.get(idsolicitacao=v_solicitacao.idsolicitacao)
        arr_cliente[index].prioridade = v_solicitacao.prioridade
        arr_cliente[index].status = v_solicitacaostatus.idstatus
    
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
        dados['cliente']= Cliente.objects.get(idcliente=idcliente)
        
        
    return render(request, 'pagecliente.html',dados)

@login_required(login_url='/login/')
def update_cliente(request, idcliente):
    statuscliente = request.GET.get('status')
    prioridadecliente = request.GET.get('prioridade')
    faq_enviar = request.GET.get('faq_enviado')
    resposta_usuario = request.POST.get('resposta_usuario')
    
    if statuscliente:
        v_solicitacao = Solicitacao.objects.get(idcliente=idcliente)
        v_solicitacaostatus = Solicitacaostatus.objects.get(idsolicitacao=v_solicitacao.idsolicitacao)
        v_solicitacaostatus.idstatus = statuscliente
        v_solicitacaostatus.save()
        return redirect('/')
    
    if prioridadecliente:
        v_solicitacao = Solicitacao.objects.get(idcliente=idcliente)
        v_solicitacao.prioridade = prioridadecliente
        v_solicitacao.save()
        return redirect('/')
    
    if faq_enviar:
        v_faq_enviar = Cliente.objects.get(idcliente=idcliente)
        v_faq_enviar.faq_enviar = faq_enviar
        v_faq_enviar.save()
        
        return redirect('/')
    
    
    if request.method == 'POST':
        cliente = Cliente.objects.get(idcliente=idcliente)
        resposta_usuario = request.POST.get('resposta_usuario')
        cliente.resposta_usuario = resposta_usuario

        # Renderizar o template do e-mail
        context = {
            'cliente': cliente,
            'resposta_usuario': resposta_usuario,
        }
        html_message = render_to_string('pageclienteX.html', context)
        text_message = strip_tags(html_message)

        # Anexar a imagem embutida ao e-mail
        image_path = os.path.join(settings.BASE_DIR, 'static', 'img', 'amm-navbar-fnt.png')
        with open(image_path, 'rb') as f:
            image_data = f.read()
        image = MIMEImage(image_data)
        image.add_header('Content-ID', '<logo_image>')
        image.add_header('Content-Disposition', 'inline', filename='amm-navbar-fnt.png')

        # Atualizar o conteúdo do e-mail para incluir a imagem embutida
        html_message = html_message.replace('src="logo_image"', f'src="cid:logo_image"')

        # Enviar e-mail para o cliente
        subject = f'Resposta ao seu chamado: {cliente.assunto}' 
        from_email = 'teushiftz@gmail.com'  
        to_email = cliente.email_cliente  

        email = EmailMultiAlternatives(subject, text_message, from_email, [to_email])
        email.attach_alternative(html_message, "text/html")
        email.attach(image)

        # Processar o anexo enviado pelo usuário, se existir
        anexo = request.FILES.get('anexo')
        if anexo:
            email.attach(anexo.name, anexo.read(), anexo.content_type)

        email.send()
        cliente.save()
        return redirect('/')

    return redirect(request.path_info)


def cliente_page_submit(request):
    if request.method == 'POST':
        nomecliente = request.POST.get('nomecliente')
        cpf_cnpj = request.POST.get('cpf_cnpj')
        email_cliente = request.POST.get('email_cliente')
        telefone_cliente = request.POST.get('telefone_cliente')
        descricao = request.POST.get('descricao')
        assunto = request.POST.get('assunto')
        


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
                 
    return  render(request, 'formshd.html')


def faq_amm(request):
    query = request.GET.get('q')  # Obtém o parâmetro de pesquisa da URL

    if query:
        # Realize a pesquisa no banco de dados usando a sua lógica
        clientes = Cliente.objects.filter(
            Q(assuntoicontains=query) | Q(descricaoicontains=query)
        )
    else:
        # Se nenhum parâmetro de pesquisa for fornecido, retorne todos os clientes
        clientes = Cliente.objects.all()

    dados = {'clientes': clientes, 'query': query}
    return render(request, 'FAQ.html', dados)