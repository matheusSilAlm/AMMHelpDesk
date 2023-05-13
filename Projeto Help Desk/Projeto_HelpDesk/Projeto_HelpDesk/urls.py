
from django.urls import path
from app_helpdesk import views

urlpatterns = [
    #rota, view responsavel, nome de referencia
    # 
    path('',views.home,name='home')
]
