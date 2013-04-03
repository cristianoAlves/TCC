from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    #Login
    url(r'^$', 'django.contrib.auth.views.login'),
    url(r'^admin/', include(admin.site.urls)),     
    url(r'^gerenciador_testes/login/$', 'django.contrib.auth.views.login'),
    url(r'^gerenciador_testes/logout/$', 'gerenciador_testes.views.logoutRequest'),
    
    #visao geral do projeto   
    url(r'^gerenciador_testes/visao_geral/$', 'gerenciador_testes.views.visao_geral'),     
    url(r'^gerenciador_testes/projeto/(?P<projeto_id>\d+)/visao_geral/', 'gerenciador_testes.views.visao_geral'),
    
    #testes por projeto e geral
    url(r'^gerenciador_testes/projeto/testes_no_projeto/', 'gerenciador_testes.views.testes_no_projeto'),
    url(r'^gerenciador_testes/projeto/(?P<projeto_id>\d+)/testes_no_projeto/', 'gerenciador_testes.views.testes_no_projeto'),
    
    #lista de projetos
    url(r'^gerenciador_testes/projeto/$', 'gerenciador_testes.views.lista_projeto'),
    
    #controle de execucao   
    url(r'^gerenciador_testes/(?P<casoDeTeste_id>\d+)/$', 'gerenciador_testes.views.detail'),
    url(r'^gerenciador_testes/(?P<casoDeTeste_id>\d+)/registra/cancelar$', 'gerenciador_testes.views.registra_cancelar'),
    url(r'^gerenciador_testes/(?P<casoDeTeste_id>\d+)/registra/passou$', 'gerenciador_testes.views.registra_passou'),
    url(r'^gerenciador_testes/(?P<casoDeTeste_id>\d+)/registra/falhou$', 'gerenciador_testes.views.registra_falhou'),
    url(r'^gerenciador_testes/(?P<casoDeTeste_id>\d+)/registra/sikuli$', 'gerenciador_testes.views.registra_sikuli'),
    
)
