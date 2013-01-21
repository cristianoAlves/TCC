from gerenciador_testes.models import CasoDeTeste, CasoDeTestePasso, Status, Execucao
from django.contrib import admin

admin.site.register(CasoDeTeste)
admin.site.register(CasoDeTestePasso)
admin.site.register(Status)
admin.site.register(Execucao)