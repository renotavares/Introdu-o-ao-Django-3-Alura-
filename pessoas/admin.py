from django.contrib import admin
from .models import Pessoa

class ListPessoas(admin.ModelAdmin):
    list_display = ('id','nome','email')
    list_display_links = ('id', 'nome')
    search_fields = ('nome',)

admin.site.register(Pessoa, ListPessoas)