from datetime import datetime

from django.contrib.auth.models import User
from django.db import models


class Receita(models.Model):
    nome = models.CharField(max_length=200)
    ingredientes = models.TextField()
    modo_preparo = models.TextField()
    tempo_preparo = models.IntegerField()
    rendimento = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    data = models.DateTimeField(default=datetime.now, blank=True)
    foto = models.ImageField(upload_to='imgs/%d/%m/%Y/', blank=True)
    pessoa = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    def __str__(self):
        return self.nome