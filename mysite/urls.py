from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Login
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^gerenciador_testes/login/$', 'django.contrib.auth.views.login'),
    url(r'^gerenciador_testes/logout/$', 'gerenciador_testes.views.logoutRequest'),
    
    #TODO:    - receber o projeto_id;
    #         - mudar o nome da view para lista_todos_casos_testes
    url(r'^gerenciador_testes/projeto/testes_no_projeto/', 'gerenciador_testes.views.testes_no_projeto'),
    
    #TODO: mudar o nome da view para lista_casos_teste_por_projeto
    url(r'^gerenciador_testes/projeto/(?P<projeto_id>\d+)/testes_no_projeto', 'gerenciador_testes.views.testes_no_projeto'),
    
    url(r'^gerenciador_testes/projeto/(?P<projeto_id>\d+)/lista_testes_para_inserir_no_projeto$', 'gerenciador_testes.views.lista_testes_para_inserir_no_projeto'),
    url(r'^gerenciador_testes/projeto/(?P<projeto_id>\d+)', 'gerenciador_testes.views.visao_geral', name='url_visao_geral'),
    url(r'^gerenciador_testes/projeto/$', 'gerenciador_testes.views.lista_projeto'),
    url(r'^gerenciador_testes/(?P<projeto_id>\d+)/(?P<casoDeTeste_id>\d+)/remover_do_projeto$', 'gerenciador_testes.views.remover_do_projeto'),

    url(r'^gerenciador_testes/(?P<casoDeTeste_id>\d+)/deletar$', 'gerenciador_testes.views.remover_teste'),
    url(r'^gerenciador_testes/(?P<casoDeTeste_id>\d+)/$', 'gerenciador_testes.views.detail'),
    url(r'^gerenciador_testes/(?P<casoDeTeste_id>\d+)/registra/cancelar$', 'gerenciador_testes.views.registra_cancelar'),
    url(r'^gerenciador_testes/(?P<casoDeTeste_id>\d+)/registra/passou$', 'gerenciador_testes.views.registra_passou'),
    url(r'^gerenciador_testes/(?P<casoDeTeste_id>\d+)/registra/falhou$', 'gerenciador_testes.views.registra_falhou'),
    url(r'^gerenciador_testes/(?P<casoDeTeste_id>\d+)/registra/sikuli$', 'gerenciador_testes.views.registra_sikuli'),
    
    
)
