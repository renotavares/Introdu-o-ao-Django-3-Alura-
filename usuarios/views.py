from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import auth, messages
from django.contrib.auth.models import User

from receitas.models import Receita


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
        receitas = Receita.objects\
            .order_by('-data')\
            .filter(status=True, pessoa=request.user.id)
        dados ={
            'receitas': receitas
        }
        return render(request, 'usuarios/dashboard.html',dados)
    return redirect('login')

def logout(request):
    auth.logout(request)
    return redirect('index')

def cria_receita(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            nome_receita = request.POST['nome_receita']
            ingredientes = request.POST['ingredientes']
            modo_preparo = request.POST['modo_preparo']
            tempo_preparo = request.POST['tempo_preparo']
            rendimento = request.POST['rendimento']
            categoria = request.POST['categoria']
            foto_receita = request.FILES['foto_receita']
            user = get_object_or_404(User, pk=request.user.id)
            receita = Receita.objects\
                .create(nome = nome_receita,
                        ingredientes = ingredientes,
                        modo_preparo = modo_preparo,
                        tempo_preparo = tempo_preparo,
                        rendimento = rendimento,
                        categoria = categoria,
                        foto = foto_receita,
                        pessoa = user,
                        status = True)
            receita.save()
            return redirect('dashboard')
        return render(request, 'usuarios/cria_receita.html')
    return redirect('login')