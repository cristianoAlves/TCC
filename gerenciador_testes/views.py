from django.template import Context
from django.template import RequestContext
from django.http import HttpResponseRedirect
from gerenciador_testes.models import casoDeTeste, casoDeTestePasso
from django.shortcuts import render_to_response
from django.contrib import auth
from forms import CasoDeTesteForm
from django.utils.datastructures import MultiValueDictKeyError



def logoutRequest(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/gerenciador_testes/login')    

def principal(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')
    
    form_has_any_error = False
    
    listaCasoTestes = casoDeTeste.objects.all()        
    if request.method == 'POST':  # If the form has been submitted...
        form = CasoDeTesteForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            titulo_post = form.cleaned_data['titulo']
            caminho_post = form.cleaned_data['caminhoSikuli']
            casoDeTeste_obj = casoDeTeste(titulo=titulo_post, caminhoSikuli=caminho_post)
            casoDeTeste_obj.save()
            return HttpResponseRedirect('../../gerenciador_testes/principal')
        else:
            form_has_any_error = True
    else:    
        form = CasoDeTesteForm()
    
    c = Context({
                 'listaCasoTestes': listaCasoTestes,
                 'form': form,
                 'form_has_any_errors' : form_has_any_error,
    })
        
    return render_to_response('gerenciador_testes/principal.html',
                              c,
                              context_instance=RequestContext(request))
    

def registra_passou (request, casoDeTeste_id):
    print "O teste %s passou!!" % casoDeTeste_id
    return HttpResponseRedirect('/gerenciador_testes/login')

def detail(request, casoDeTeste_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')
    
    listaDePassos = casoDeTestePasso.objects.filter(casoDeTeste__exact=casoDeTeste_id)
    casoTesteNome = casoDeTeste.objects.get(pk=casoDeTeste_id).titulo
    
    ex = None
    
    try:
        if 'executar' in request.GET.keys():
            ex = True
    except MultiValueDictKeyError:
        pass
    
    c = Context({
        'listaDePassos': listaDePassos,
        'casoTesteNome': casoTesteNome,
        'ex': ex,
        
    })
    return render_to_response('gerenciador_testes/detail.html',
                              c,
                              context_instance=RequestContext(request))
    
