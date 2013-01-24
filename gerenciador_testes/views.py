from django.template import Context
from django.template import RequestContext
from django.http import HttpResponseRedirect
from gerenciador_testes.models import casoDeTeste, casoDeTestePasso
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib import auth
from forms import CasoDeTesteForm



def logoutRequest(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/gerenciador_testes/login')    

def principal(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')
    listaCasoTestes = casoDeTeste.objects.all()
    form =  CasoDeTesteForm()  
    c = Context({
        'listaCasoTestes': listaCasoTestes,
        'form': form,
    })
    return render_to_response('gerenciador_testes/principal.html',
                              c,
                              context_instance=RequestContext(request))
    

def detail(request, casoDeTeste_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')
    listaDePassos = casoDeTestePasso.objects.filter(casoDeTeste__exact=casoDeTeste_id)
    casoTesteNome = casoDeTeste.objects.get(pk=casoDeTeste_id).titulo

    c = Context({
        'listaDePassos': listaDePassos,
        'casoTesteNome': casoTesteNome,
    })
    return render_to_response('gerenciador_testes/detail.html',
                              c,
                              context_instance=RequestContext(request))

def adicionaCasoDeTeste(request):
    if request.method == 'POST':                        # If the form has been submitted...
        form = CasoDeTesteForm(request.POST)            # A form bound to the POST data
        if form.is_valid():                             # All validation rules pass
            titulo_post = request.POST.get('titulo')
            caminho_post = request.POST.get('caminhoSikuli')
            casoDeTeste_obj = casoDeTeste(titulo=titulo_post, caminhoSikuli=caminho_post)
            casoDeTeste_obj.save()
            # ...
            return HttpResponseRedirect('../../gerenciador_testes/principal')     # Redirect after POST
    else:
        form = CasoDeTesteForm()                            # An unbound form

    return render_to_response('gerenciador_testes/',
                              {'form': form},
                              context_instance=RequestContext(request))



