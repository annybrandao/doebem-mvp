
from django.db import models


class Campanha(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    data_inicio = models.DateField()
    data_fim = models.DateField(null=True, blank=True)
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

    @property
    def total_doado(self):
        return sum(d.quantidade for d in self.doacoes.all())

    @property
    def total_entregue(self):
        return sum(e.quantidade for e in self.entregas.all())

    @property
    def disponivel(self):
        return self.total_doado - self.total_entregue


class Doacao(models.Model):
    campanha = models.ForeignKey(
        Campanha, on_delete=models.CASCADE, related_name="doacoes"
    )
    doador = models.CharField(max_length=100)
    tipo_agasalho = models.CharField(max_length=100, default="Não informado")
    quantidade = models.PositiveIntegerField()
    descricao = models.CharField(max_length=200, blank=True)
    data = models.DateField()

    def __str__(self):
        return f"{self.doador} - {self.quantidade} peça(s)"


class Entrega(models.Model):
    campanha = models.ForeignKey(
        Campanha, on_delete=models.CASCADE, related_name="entregas"
    )
    beneficiario = models.CharField(max_length=100)
    tipo_agasalho = models.CharField(max_length=100, default="Não informado")
    quantidade = models.PositiveIntegerField()
    data = models.DateField()

    def __str__(self):
        return f"{self.beneficiario} - {self.quantidade} peça(s)"

