from django.contrib import admin
from app_helpdesk.models import Cliente, Usuario, Solicitacao

# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('idcliente','nomecliente','email_cliente','assunto','descricao','datacriacao')
    list_filter = ('idcliente',)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('idusuario','nomeusuario','setor','turno')
    list_display = ('idusuario','nomeusuario')

class SolicitacaoAdmin(admin.ModelAdmin):
    list_display = ('idsolicitacao','data_solicitacao')
    # list_filter = ('idsoliticacao', 'data_solicitacao',)



admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Usuario,UsuarioAdmin)
admin.site.register(Solicitacao,SolicitacaoAdmin)