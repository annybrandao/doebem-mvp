from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Campanha, Doacao, Entrega

admin.site.register(Campanha)
admin.site.register(Doacao)
admin.site.register(Entrega)