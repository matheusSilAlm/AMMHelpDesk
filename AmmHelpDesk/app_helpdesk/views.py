from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from app_helpdesk.models import Cliente, Solicitacao, Solicitacaostatus, models
from django.shortcuts import render
from django.db import transaction
from django.http import HttpResponse

#Usuário faz login na pagina.
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
    arr_cliente = Cliente.objects.all()
    
    for index, cliente in enumerate(arr_cliente, start=0):
        v_solicitacao = Solicitacao.objects.get(idcliente=arr_cliente[index].idcliente)
        v_solicitacaostatus = Solicitacaostatus.objects.get(idsolicitacao=v_solicitacao.idsolicitacao)
        arr_cliente[index].prioridade = v_solicitacao.prioridade
        arr_cliente[index].status = v_solicitacaostatus.idstatus
    
    cliente = {
        'clientes': arr_cliente
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
def atender_cliente(request):
    idcliente = request.GET.get('id')
    dados = {}
    if idcliente:
        dados['cliente']= Cliente.objects.get(idcliente=idcliente)
        
        Cliente.objects.filter(idcliente=idcliente).update()
    return render(request, 'pagecliente.html',dados)





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
                 
    return HttpResponse('Dados salvos com sucesso!')

