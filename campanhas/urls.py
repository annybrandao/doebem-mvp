
from django.urls import path
from . import views

app_name = "campanhas"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("movimentacao/", views.movimentacao, name="movimentacao"),
]