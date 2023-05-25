from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 


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