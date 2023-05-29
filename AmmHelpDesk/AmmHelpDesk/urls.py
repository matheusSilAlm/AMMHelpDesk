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
    path('formshd/', views.cliente_page)
]
