from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.models import User

from apps.receitas.models import Receita


def cadastro(request):
  if request.method == 'POST':
    nome = request.POST['nome']
    email = request.POST['email']
    senha = request.POST['senha']
    if User.objects.filter(email=email).exists():
      messages.error(request, 'Já existe um usuário com esse e-mail')
      return redirect('cadastro')
    user = User.objects.create_user(username=nome,
                                    email=email,
                                    password=senha)
    user.save()
    return redirect('login')
  return render(request, 'usuarios/cadastro.html')

def login(request):
  if request.method == 'POST':
    email = request.POST['email']
    senha = request.POST['senha']
    if User.objects.filter(email=email).exists():
      nome = User.objects.filter(email=email).values_list('username', flat=True).get()
      user = auth.authenticate(request, username=nome, password=senha)
      if user is not None:
        auth.login(request, user)
        return redirect('dashboard')
    messages.error(request, 'Usuário e/ou senha inválido(s)')
  return render(request, 'usuarios/login.html')

def dashboard(request):
  if request.user.is_authenticated:
    receitas = Receita.objects \
      .order_by('-data') \
      .filter(status=True, pessoa=request.user.id)
    dados ={
      'receitas': receitas
    }
    return render(request, 'usuarios/dashboard.html',dados)
  return redirect('login')

def logout(request):
  auth.logout(request)
  return redirect('index')