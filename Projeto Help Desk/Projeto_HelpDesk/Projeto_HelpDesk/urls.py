from django.contrib import admin
from django.urls import path
from app_helpdesk import views

urlpatterns = [
    #rota, view responsavel, nome de referencia
    # 
    path('AMMHelpDesk/', views.Cliente)

]