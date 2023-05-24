from django.shortcuts import render, redirect
from app_helpdesk.models import Cliente
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages   



def Cliente(request):
    nomecliente = request.get('Nome Completo')
