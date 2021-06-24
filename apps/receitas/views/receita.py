from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from apps.receitas.models import Receita
from django.core.paginator import Paginator


def index(request):
    receitas = Receita.objects.order_by('-data').filter(status=True)
    paginator = Paginator(receitas, 3)
    pagina = request.GET.get('page')
    receitas_por_pagina = paginator.get_page(pagina)

    dados = {
        'receitas' : receitas_por_pagina
    }

    return render(request, 'receitas/index.html', dados)

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    informacoes_da_receita = {
        'receita' : receita
    }

    return render(request, 'receitas/receita.html', informacoes_da_receita)

def buscar(request):
    receitas = Receita.objects.order_by('-data').filter(status=True)

    if 'buscar' in request.GET:
        nome_receita = request.GET['buscar']
        receitas = receitas.filter(nome__icontains=nome_receita)

    dados = {
        'receitas' : receitas
    }

    return render(request, 'receitas/buscar.html', dados)

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
      receita = Receita.objects \
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
    return render(request, 'receitas/cria_receita.html')
  return redirect('login')

def deleta_receita(request, receita_id):
  receita = get_object_or_404(Receita, pk=receita_id)
  receita.delete()
  return redirect('dashboard')

def edita_receita(request, receita_id):
  receita = get_object_or_404(Receita, pk=receita_id)
  receita_a_editar = {
    'receita': receita
  }
  return render(request, 'receitas/edita_receita.html', receita_a_editar)

def atualiza_receita(request):
  if request.method == 'POST':
    receita = get_object_or_404(Receita, pk=request.POST['receita_id'])
    receita.nome = request.POST['nome_receita']
    receita.ingredientes = request.POST['ingredientes']
    receita.modo_preparo = request.POST['modo_preparo']
    receita.tempo_preparo = request.POST['tempo_preparo']
    receita.rendimento = request.POST['rendimento']
    receita.categoria = request.POST['categoria']
    if 'foto_receita' in request.FILES:
      receita.foto = request.FILES['foto_receita']
    receita.save()
  return redirect('dashboard')