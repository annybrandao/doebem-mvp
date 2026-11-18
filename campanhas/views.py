
from datetime import date

from django.contrib import messages
from django.db import transaction
from django.db.models import Sum
from django.shortcuts import render, redirect

from .models import Campanha, Doacao, Entrega


def inicio(request):
    campanhas = Campanha.objects.filter(ativa=True).order_by("-data_inicio")
    return render(request, "campanhas/inicio.html", {
        "campanhas": campanhas
    })


def movimentacao(request):
    campanhas = Campanha.objects.filter(ativa=True)

    if request.method == "POST":
        try:
            tipo = request.POST.get("tipo")
            campanha_id = request.POST.get("campanha")
            tipo_agasalho = request.POST.get("tipo_agasalho", "").strip()
            quantidade = int(request.POST.get("quantidade", "0"))
            data_movimento = date.fromisoformat(request.POST.get("data", ""))
            pessoa = request.POST.get("pessoa", "").strip()

            campanha = campanhas.get(id=campanha_id)

            if tipo not in ["doacao", "entrega"]:
                raise ValueError("Selecione doação ou entrega.")

            if not tipo_agasalho or not pessoa:
                raise ValueError("Preencha todos os campos.")

            if quantidade <= 0:
                raise ValueError("A quantidade deve ser maior que zero.")

            with transaction.atomic():
                if tipo == "doacao":
                    Doacao.objects.create(
                        campanha=campanha,
                        doador=pessoa,
                        tipo_agasalho=tipo_agasalho,
                        quantidade=quantidade,
                        data=data_movimento,
                    )
                else:
                    recebidas = Doacao.objects.filter(
                        campanha=campanha,
                        tipo_agasalho__iexact=tipo_agasalho
                    ).aggregate(total=Sum("quantidade"))["total"] or 0

                    entregues = Entrega.objects.filter(
                        campanha=campanha,
                        tipo_agasalho__iexact=tipo_agasalho
                    ).aggregate(total=Sum("quantidade"))["total"] or 0

                    saldo = recebidas - entregues

                    if quantidade > saldo:
                        raise ValueError(
                            f"Estoque insuficiente. Saldo disponível: {saldo}."
                        )

                    Entrega.objects.create(
                        campanha=campanha,
                        beneficiario=pessoa,
                        tipo_agasalho=tipo_agasalho,
                        quantidade=quantidade,
                        data=data_movimento,
                    )

            recebidas = Doacao.objects.filter(
                campanha=campanha,
                tipo_agasalho__iexact=tipo_agasalho
            ).aggregate(total=Sum("quantidade"))["total"] or 0

            entregues = Entrega.objects.filter(
                campanha=campanha,
                tipo_agasalho__iexact=tipo_agasalho
            ).aggregate(total=Sum("quantidade"))["total"] or 0

            return render(request, "campanhas/sucesso.html", {
                "campanha": campanha,
                "tipo": "Doação" if tipo == "doacao" else "Entrega",
                "tipo_agasalho": tipo_agasalho,
                "quantidade": quantidade,
                "saldo": recebidas - entregues,
            })

        except (ValueError, TypeError, Campanha.DoesNotExist) as erro:
            messages.error(request, str(erro))

    return render(request, "campanhas/movimentacao.html", {
        "campanhas": campanhas,
        "hoje": date.today().isoformat(),
    })
