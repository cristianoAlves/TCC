from django.template import Context
from django.template import RequestContext
from django.http import HttpResponseRedirect
from gerenciador_testes.models import casoDeTeste, casoDeTestePasso, projeto, casoDeTesteEmProjeto
from django.shortcuts import render_to_response
from django.contrib import auth
from forms import CasoDeTesteForm, ProjetoForm
from django.utils.datastructures import MultiValueDictKeyError
import subprocess




def logoutRequest(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/gerenciador_testes/login')    

def lista_projeto(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')
    
    form_has_any_error = False
    
    listaProjetos = projeto.objects.all()
    if request.method == 'POST':                # If the form has been submitted...
        formProj = ProjetoForm(request.POST)        # A form bound to the POST data
        if formProj.is_valid():                     # All validation rules pass
            nome_post = formProj.cleaned_data['nomeProjeto']
            data_post = formProj.cleaned_data['dataAbertura']
            projeto_obj = projeto(nomeProjeto=nome_post, dataAbertura=data_post)
            projeto_obj.save()
            return HttpResponseRedirect('../../gerenciador_testes/projeto')
        else:
            form_has_any_error = True
    else:    
        formProj = ProjetoForm()
    
    c = Context({
                 'listaProjetos': listaProjetos,
                 'formProj': formProj,
                 'form_has_any_errors' : form_has_any_error,
    })
        
    return render_to_response('gerenciador_testes/projeto.html',
                              c,
                              context_instance=RequestContext(request))

def principal(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')
    
    form_has_any_error = False
    
    listaCasoTestes = casoDeTeste.objects.all()
    if request.method == 'POST':                # If the form has been submitted...
        form = CasoDeTesteForm(request.POST)    # A form bound to the POST data
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

def registra_cancelar (request, casoDeTeste_id):    
    return HttpResponseRedirect('/gerenciador_testes/principal')

def registra_passou (request, casoDeTeste_id):    
    return HttpResponseRedirect('/gerenciador_testes/principal')

def registra_falhou (request, casoDeTeste_id):   
    return HttpResponseRedirect('/gerenciador_testes/principal')

def registra_sikuli (request, casoDeTeste_id):
    casoTeste = casoDeTeste.objects.get(pk=casoDeTeste_id)
    sikuliPath = 'C:\\"Program Files (x86)\\Sikuli X\\Sikuli-IDE.bat" -r '
    caminhoTesteSikuli = casoTeste.caminhoSikuli
    subprocess.Popen(sikuliPath + caminhoTesteSikuli, shell=True)
    
    print ("==============sikuli===================\n")
    print (casoTeste.caminhoSikuli)
    print (sikuliPath + caminhoTesteSikuli)
    return HttpResponseRedirect('/gerenciador_testes/1/?executar')

def detail(request, casoDeTeste_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')
    
    listaDePassos = casoDeTestePasso.objects.filter(casoDeTeste__exact=casoDeTeste_id)
    # casoTesteNome = casoDeTeste.objects.get(pk=casoDeTeste_id).titulo
    casoTeste = casoDeTeste.objects.get(pk=casoDeTeste_id)
    ex = None
    
    try:
        if 'executar' in request.GET.keys():
            ex = True
    except MultiValueDictKeyError:
        pass
    
    c = Context({
        'listaDePassos': listaDePassos,
        'casoTeste': casoTeste,
        'ex': ex,
        
    })
    return render_to_response('gerenciador_testes/detail.html',
                              c,
                              context_instance=RequestContext(request))
    
def visao_geral(request, projeto_id=1):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')
    
    meuProjeto = projeto.objects.get(pk=projeto_id)
    totalProjetos = projeto.objects.all().count()
    totalTesteEmProjeto = casoDeTeste.objects.filter(casodetesteemprojeto__projeto__exact=projeto_id).count()
    ultimaExecucao = 'falhou'
    acumuladoFalhas = '5.7%'
    acumuladoSucesso = '94.3%'
    
    c = Context({
                 'meuProjeto': meuProjeto,
                 'totalProjetos': totalProjetos,
                 'totalTesteEmProjeto': totalTesteEmProjeto,
                 'ultimaExecucao' : ultimaExecucao,
                 'acumuladoFalhas': acumuladoFalhas,
                 'acumuladoSucesso': acumuladoSucesso,
    })
        
    return render_to_response('gerenciador_testes/visao_geral.html',
                              c,
                              context_instance=RequestContext(request))
