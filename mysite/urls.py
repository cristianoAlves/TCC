from django.conf.urls import patterns, include, url


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'gerenciador_testes.views.principal'),
    url(r'^gerenciador_testes/login/$', 'django.contrib.auth.views.login'),
    url(r'^gerenciador_testes/principal/$', 'gerenciador_testes.views.principal'),
    url(r'^gerenciador_testes/(?P<casoDeTeste_id>\d+)/$', 'gerenciador_testes.views.detail'),
    url(r'^gerenciador_testes/(?P<casoDeTeste_id>\d+)/passos/$', 'gerenciador_testes.views.passos'),
    url(r'^admin/', include(admin.site.urls)),
)
