from django.contrib import admin
from django.urls import path
from app_helpdesk import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('helpdeskAmm/', views.cliente_solicitacao)
     path('login/', views.login_user)
]
