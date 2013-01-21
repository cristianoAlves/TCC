from django.template import Context, loader
from gerenciador_testes.models import CasoDeTeste, CasoDeTestePasso
from django.http import HttpResponse

def index(RequestContext):
    listaCasoTestes = CasoDeTeste.objects.all()
    t = loader.get_template('gerenciador_testes/index.html')
    c = Context({
        'listaCasoTestes': listaCasoTestes,
    })
    return HttpResponse(t.render(c))

def detail(request, CasoDeTeste_id):
    listaDePassos = CasoDeTestePasso.objects.filter(caso_teste__exact=CasoDeTeste_id)
    CasoTesteNome = CasoDeTeste.objects.get(pk=CasoDeTeste_id).titulo
    t = loader.get_template('gerenciador_testes/detail.html')
    c = Context({
        'listaDePassos': listaDePassos,
        'CasoTesteNome': CasoTesteNome,
    })
    return HttpResponse(t.render(c))

def passos(request, CasoDeTeste_id):
    return HttpResponse("You're looking at the passos of caso de teste %s." % CasoDeTeste_id)


