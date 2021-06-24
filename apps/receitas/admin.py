from django.contrib import admin
from .models import Receita

class ListReceitas(admin.ModelAdmin):
    list_display = ('id','nome','status')
    list_display_links = ('id', 'nome')
    list_editable = ('status',)
    search_fields = ('nome',)

admin.site.register(Receita, ListReceitas)
