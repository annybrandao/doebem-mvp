from datetime import date

from django.test import TestCase

from .models import Campanha, Doacao, Entrega


class CampanhaTestCase(TestCase):

    def setUp(self):
        self.campanha = Campanha.objects.create(
            nome="Campanha do Agasalho 2026",
            descricao="Arrecadação de agasalhos",
            data_inicio=date(2026, 11, 1),
            ativa=True,
        )

    def test_criar_campanha(self):
        self.assertEqual(
            self.campanha.nome,
            "Campanha do Agasalho 2026"
        )
        self.assertTrue(self.campanha.ativa)

    def test_total_doado(self):
        Doacao.objects.create(
            campanha=self.campanha,
            doador="Voluntário 1",
            quantidade=10,
            data=date(2026, 11, 10),
        )

        Doacao.objects.create(
            campanha=self.campanha,
            doador="Voluntário 2",
            quantidade=5,
            data=date(2026, 11, 11),
        )

        self.assertEqual(self.campanha.total_doado, 15)

    def test_total_entregue(self):
        Entrega.objects.create(
            campanha=self.campanha,
            beneficiario="Beneficiário 1",
            quantidade=4,
            data=date(2026, 11, 12),
        )

        self.assertEqual(self.campanha.total_entregue, 4)

    def test_calcular_saldo_disponivel(self):
        Doacao.objects.create(
            campanha=self.campanha,
            doador="Voluntário 1",
            quantidade=20,
            data=date(2026, 11, 10),
        )

        Entrega.objects.create(
            campanha=self.campanha,
            beneficiario="Beneficiário 1",
            quantidade=8,
            data=date(2026, 11, 12),
        )

        self.assertEqual(self.campanha.disponivel, 12)

    def test_criar_doacao_e_entrega(self):
        doacao = Doacao.objects.create(
            campanha=self.campanha,
            doador="Voluntário",
            quantidade=10,
            data=date(2026, 11, 10),
        )

        entrega = Entrega.objects.create(
            campanha=self.campanha,
            beneficiario="Beneficiário",
            quantidade=3,
            data=date(2026, 11, 12),
        )

        self.assertEqual(doacao.campanha, self.campanha)
        self.assertEqual(entrega.campanha, self.campanha)
        self.assertEqual(self.campanha.disponivel, 7)
