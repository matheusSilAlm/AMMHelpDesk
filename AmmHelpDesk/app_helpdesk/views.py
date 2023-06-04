from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from app_helpdesk.models import Cliente, Solicitacao, Solicitacaostatus, models
from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse


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

            ########################################################################################################

# def cliente_page_submit(request):        
#     if request.POST:
#         Cliente.objects.create(
#         nomecliente = request.POST.get('nomecliente'),
#         cpf_cnpj = request.POST.get('cpf_cnpj'),
#         email_cliente  = request.POST.get('email_cliente'),
#         telefone_cliente = request.POST.get('telefone_cliente'),
#         descricao = request.POST.get('descricao'),
#         assunto = request.POST.get('assunto')
#         )
#         Solicitacao.objects.create(
#         prioridade=request.POST.get('prioridade')
#         )
#         Solicitacaostatus.objects.create(
#         idstatus=request.POST.get('idstatus')
#         )
        
#     return redirect('/')

    ########################################################################################################
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

    

def cliente_novo(request):
    novo_cliente = Cliente()
    novo_cliente.nomecliente = request.POST.get('nomecliente')
    novo_cliente.assunto = request.POST.get('assunto')

    cliente = {
        'cliente': Cliente.objects.all()
    }
    return render(request, '/', cliente)

@login_required(login_url='/login/')
def atender_cliente(request, idcliente):
    if idcliente:
        cliente=Cliente.objects.all()


   

    return render(request, 'pagecliente.html')





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

            Solicitacao.objects.create(
                prioridade='A DEFINIR'
            )
            Solicitacaostatus.objects.create(
                idstatus='ABERTO'
            )        
    return HttpResponse('Dados salvos com sucesso!')

