from django.contrib import admin
from app_helpdesk.models import Cliente, Usuario

# Register your models here.
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('idcliente','nomecliente','email_cliente','assunto','descricao')
    list_filter = ('idcliente',)

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('idusuario','nomeusuario','setor','turno')
    list_display = ('idusuario','nomeusuario')

admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Usuario,UsuarioAdmin)