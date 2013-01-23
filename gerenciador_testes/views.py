from django.template import Context, loader
from django.template import RequestContext
from gerenciador_testes.models import casoDeTeste, casoDeTestePasso
from django.http import HttpResponse
from django.shortcuts import render_to_response


def login(request):       
    c = Context({
        'listaCasoTestes': 'ok',
    })
    return render_to_response('gerenciador_testes/login.html',
                              c,
                              context_instance=RequestContext(request))
def principal(request):
    listaCasoTestes = casoDeTeste.objects.all()   
    c = Context({
        'listaCasoTestes': listaCasoTestes,
    })
    return render_to_response('gerenciador_testes/principal.html',
                              c,
                              context_instance=RequestContext(request))
    

def detail(request, casoDeTeste_id):
    listaDePassos = casoDeTestePasso.objects.filter(casoDeTeste__exact=casoDeTeste_id)
    casoTesteNome = casoDeTeste.objects.get(pk=casoDeTeste_id).titulo

    c = Context({
        'listaDePassos': listaDePassos,
        'casoTesteNome': casoTesteNome,
    })
    return render_to_response('gerenciador_testes/detail.html',
                              c,
                              context_instance=RequestContext(request))

def passos(request, casoDeTeste_id):
    return HttpResponse("You're looking at the passos of caso de teste %s." % casoDeTeste_id)


