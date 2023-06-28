from django.db import models
from django.contrib.auth.models import User



class AppHelpdeskPessoa(models.Model):
    idpessoa = models.IntegerField(db_column='IDPessoa', primary_key=True)  # Field name made lowercase.
    nomepessoa = models.CharField(db_column='NomePessoa', max_length=80)  # Field name made lowercase.
    cpf_cnpj = models.CharField(db_column='Cpf_cnpj', max_length=14)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=80)  # Field name made lowercase.
    telefone = models.CharField(db_column='Telefone', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'app_helpdesk_pessoa'


# class AuthGroup(models.Model):
#     name = models.CharField(unique=True, max_length=150)

#     class Meta:
#         managed = True
#         db_table = 'auth_group'


# class AuthGroupPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
#     permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

#     class Meta:
#         managed = True
#         db_table = 'auth_group_permissions'
#         unique_together = (('group', 'permission'),)


# class AuthPermission(models.Model):
#     name = models.CharField(max_length=255)
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
#     codename = models.CharField(max_length=100)

#     class Meta:
#         managed = True
#         db_table = 'auth_permission'
#         unique_together = (('content_type', 'codename'),)


# class AuthUser(models.Model):
#     password = models.CharField(max_length=128)
#     last_login = models.DateTimeField(blank=True, null=True)
#     is_superuser = models.IntegerField()
#     username = models.CharField(unique=True, max_length=150)
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.CharField(max_length=254)
#     is_staff = models.IntegerField()
#     is_active = models.IntegerField()
#     date_joined = models.DateTimeField()

#     class Meta:
#         managed = True
#         db_table = 'auth_user'


# class AuthUserGroups(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

#     class Meta:
#         managed = True
#         db_table = 'auth_user_groups'
#         unique_together = (('user', 'group'),)


# class AuthUserUserPermissions(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)
#     permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

#     class Meta:
#         managed = True
#         db_table = 'auth_user_user_permissions'
#         unique_together = (('user', 'permission'),)


class Cliente(models.Model):
    idcliente = models.AutoField(db_column='IDCliente', primary_key=True)  # Field name made lowercase.
    nomecliente = models.CharField(db_column='NomeCliente', max_length=80)  # Field name made lowercase.
    cpf_cnpj = models.CharField(db_column='Cpf_cnpj',max_length=20)  # Field name made lowercase.
    datacriacao = models.DateTimeField(auto_now=True)
    email_cliente = models.CharField(db_column='Email_Cliente', max_length=80)  # Field name made lowercase.
    telefone_cliente = models.CharField(db_column='Telefone_Cliente', max_length=20)  # Field name made lowercase.
    assunto = models.CharField(db_column='Assunto', max_length=19, blank=True, null=True)  # Field name made lowercase.
    descricao = models.TextField(db_column='Descricao', blank=True, null=True)  # Field name made lowercase.
    resposta_usuario = models.TextField(db_column='Resposta_chamado', blank=True, null=True)
    faq_enviar = models.CharField(db_column='Faq_Enviado', max_length=19 , blank=True, null=True)
    
    
    # def __str__(self):
    #     return self.nomecliente, self.cpf_cnpj, self.email_cliente, self.telefone_cliente, self.assunto, self.descricao
    

    class Meta:
        managed = True
        db_table = 'cliente'

    def get_data_criacao(self):
        return self.datacriacao.strftime('%d/%m/%Y - %H:%M')
    


# class DjangoAdminLog(models.Model):
#     action_time = models.DateTimeField()
#     object_id = models.TextField(blank=True, null=True)
#     object_repr = models.CharField(max_length=200)
#     action_flag = models.PositiveSmallIntegerField()
#     change_message = models.TextField()
#     content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
#     user = models.ForeignKey(AuthUser, models.DO_NOTHING)

#     class Meta:
#         managed = True
#         db_table = 'django_admin_log'


# class DjangoContentType(models.Model):
#     app_label = models.CharField(max_length=100)
#     model = models.CharField(max_length=100)

#     class Meta:
#         managed = True
#         db_table = 'django_content_type'
#         unique_together = (('app_label', 'model'),)


# class DjangoMigrations(models.Model):
#     id = models.BigAutoField(primary_key=True)
    # app = models.CharField(max_length=255)
#     name = models.CharField(max_length=255)
#     applied = models.DateTimeField()

#     class Meta:
#         managed = True
#         db_table = 'django_migrations'


# class DjangoSession(models.Model):
#     session_key = models.CharField(primary_key=True, max_length=40)
#     session_data = models.TextField()
#     expire_date = models.DateTimeField()

#     class Meta:
#         managed = True
#         db_table = 'django_session'


class Solicitacao(models.Model):
    idsolicitacao = models.AutoField(db_column='IDSolicitacao', primary_key=True)  # Field name made lowercase.
    idcliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='IDCliente', blank=True, null=True)  # Field name made lowercase.
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='IDUsuario', blank=True, null=True)  # Field name made lowercase.
    assunto = models.CharField(db_column='Assunto', max_length=19, blank=True, null=True)  # Field name made lowercase.
    prioridade = models.CharField(db_column='Prioridade', max_length=20, blank=True, null=True)  # Field name made lowercase.
    data_solicitacao = models.DateTimeField(db_column='Data_Solicitacao', blank=True, null=True)  # Field name made lowercase.
    solicitacaoaativo = models.CharField(db_column='SolicitacaoaAtivo', max_length=1, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.idsolicitacao

    def cor_status(self):
        if self.assunto == 'ABERTO':
            return True
        else:
            return False
    
    
    
    class Meta:
        managed = True
        db_table = 'solicitacao'


class Solicitacaostatus(models.Model):
    idsolicitacaostatus = models.AutoField(db_column='IDSolicitacaoStatus', primary_key=True)  # Field name made lowercase.
    idsolicitacao = models.ForeignKey(Solicitacao, models.DO_NOTHING, db_column='IDSolicitacao', blank=True, null=True)  # Field name made lowercase.
    idstatus = models.CharField(db_column='IDStatus', max_length=12, blank=True, null=True)  # Field name made lowercase.
    idusuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='IDUsuario', blank=True, null=True)  # Field name made lowercase.
    datastatus = models.DateTimeField(db_column='DataStatus', blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.idsolicitacaostatus, self.idsolicitacao, self.idstatus, self.idusuario, self.datastatus
    class Meta:
        managed = True
        db_table = 'solicitacaostatus'


class Usuario(models.Model):
    idusuario = models.AutoField(db_column='IDUsuario', primary_key=True)  # Field name made lowercase.
    nomeusuario = models.CharField(db_column='NomeUsuario', max_length=100)  # Field name made lowercase.
    email_usuario = models.CharField(db_column='Email_Usuario', max_length=80)  # Field name made lowercase.
    setor = models.CharField(db_column='Setor', max_length=50, blank=True, null=True)  # Field name made lowercase.
    turno = models.CharField(db_column='Turno', max_length=1, blank=True, null=True)  # Field name made lowercase.
    usuario_ativo = models.CharField(db_column='Usuario_Ativo', max_length=1, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = True
        db_table = 'usuario'