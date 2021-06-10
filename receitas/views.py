from django.shortcuts import render, get_object_or_404
from .models import Receita

def index(request):
    receitas = Receita.objects.order_by('-data').filter(status=True)

    dados = {
        'receitas' : receitas
    }

    return render(request, 'index.html', dados)

def receita(request, receita_id):
    receita = get_object_or_404(Receita, pk=receita_id)

    informacoes_da_receita = {
        'receita' : receita
    }

    return render(request, 'receita.html', informacoes_da_receita)

def buscar(request):
    receitas = Receita.objects.order_by('-data').filter(status=True)

    if 'buscar' in request.GET:
        nome_receita = request.GET['buscar']
        if nome_receita:
            receitas = receitas.filter(nome__icontains=nome_receita)

    dados = {
        'receitas' : receitas
    }

    return render(request, 'buscar.html', dados)