from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from app_helpdesk.models import Cliente, models
from django.shortcuts import render


def login_user(request):
    return render(request, 'login.html')

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
    cliente = {
        'clientes': Cliente.objects.all()
    }
    return render(request, 'listpage.html',cliente)  



def cliente_page(request):
    return render(request, 'FormsHD.html')


def cliente_page_submit(request):        
    if request.POST:
        Cliente.objects.create(
        nomecliente = request.POST.get('nomecliente'),
        cpf_cnpj = request.POST.get('cpf_cnpj'),
        email_cliente  = request.POST.get('email_cliente'),
        telefone_cliente = request.POST.get('telefone_cliente'),
        descricao = request.POST.get('descricao'),
        assunto = request.POST.get('assunto'))
    
       
    return redirect('/')
        # dados = {}
        # dados['nomecliente'] = request.POST.get('nomecliente')
        # dados['cpf_cnpj'] = request.POST.get('cpf_cnpj')
        # dados['email_cliente']  = request.POST.get('email_cliente')
        # dados['telefone_cliente'] = request.POST.get('telefone_cliente')
        # dados['descricao'] = request.POST.get('descricao')
        # Cliente.objects.create(nomecliente=dados['nomecliente'],
        #                       cpf_cnpj=int(dados['cpf_cnpj']),
        #                       email_cliente=dados['email_cliente'],
        #                       telefone_cliente=dados['telefone_cliente'],
        #                       descricao=dados['descricao'],
        #                       assunto=request.POST.get('assunto'))
    #   return redirect('/')

    
# def cliente_submit(request):
#     if request

def cliente_novo(request):
    novo_cliente = Cliente()
    novo_cliente.nomecliente = request.POST.get('nomecliente')
    novo_cliente.assunto = request.POST.get('assunto')
    #Data fica como? aula dio
    #Usuário - Tem que 
    #Status tem que deixar Aberto...
    #Prioridade tem que deixar A definir...

    cliente = {
        'cliente': Cliente.objects.all()
    }
    return render(request, '/', cliente)












#    IDCliente int primary key auto_increment,
# NomeCliente varchar(80) not null,
# Cpf_cnpj int not null,				
# Email_Cliente varchar(80) not null,
# Telefone_Cliente varchar(10) not null,
# Assunto ENUM('NOSSOS APLICATIVOS','DÚVIDAS FINANCEIRAS','SUPORTE TÉCNICO', 'RECLAMAÇÕES', 'OUTRAS INFORMAÇÕES'),
# Descricao text(300)
# );

# @login_required(login_url='/login/')
# def submit_Evento(request):
#     if request.POST:
#         titulo = request.POST.get('titulo')
#         data_evento = request.POST.get('data_evento')
#         descricao = request.POST.get('descricao')
#         usuario = request.user
#         id_evento = request.POST.get('id_evento')
#         if id_evento:
#             Evento = evento.objects.get(id=id_evento)
#             if Evento.usuario == usuario:
#                 Evento.titulo = titulo
#                 Evento.descricao = descricao
#                 Evento.data_evento = data_evento
#                 Evento.save()
#         #     evento.objects.filter(id=id_evento).update(titulo=titulo,
#         #                                                 data_evento=data_evento,
#         #                                                 descricao=descricao)
#         else:
#             evento.objects.create(titulo=titulo,
#                             data_evento=data_evento,
#                             descricao=descricao,
#                             usuario=usuario) 
#     return redirect('/')