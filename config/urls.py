from django.contrib import admin
from django.urls import path
from app_helpdesk import views
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.solicit_pages),
    path('', RedirectView.as_view(url='/home/')),
    path('login/', views.login_user),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user),
    path('formshd/', views.cliente_page),
    path('formshd/submit', views.cliente_page_submit),
    path('listpage/', views.cliente_novo),
    path('home/pagecliente/', views.atender_cliente),  
    path('home/updatecliente/<int:idcliente>/', views.update_cliente),   
    path('FAQ/', views.faq_amm, name='FAQ'),
    path('home/updatecliente/<int:idcliente>/teste/', views.update_cliente)
]
