from django.template import Context
from django.template import RequestContext
from django.http import HttpResponseRedirect
from gerenciador_testes.models import casoDeTeste, casoDeTestePasso, projeto, casoDeTesteEmProjeto
from django.shortcuts import render_to_response
from django.contrib import auth
from forms import CasoDeTesteForm, ProjetoForm
from django.utils.datastructures import MultiValueDictKeyError
import subprocess
import datetime



def logoutRequest(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/gerenciador_testes/login')

def lista_projetos(request, projeto_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')

    form_has_any_error = False

    listaProjetos = projeto.objects.all()
    meuProjeto = projeto.objects.get(pk=projeto_id)
    if request.method == 'POST':  # If the form has been submitted
        formProj = ProjetoForm(request.POST)  # A form bound to the POST data
        if formProj.is_valid():  # All validation rules pass
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
                 'meuProjeto': meuProjeto,
                 'formProj': formProj,
                 'form_has_any_errors' : form_has_any_error,
    })
        
    return render_to_response('gerenciador_testes/projeto.html',
                              c,
                              context_instance=RequestContext(request))

def lista_casos_teste_por_projeto(request, projeto_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')

    listaCasoTestes = casoDeTeste.objects.filter(casodetesteemprojeto__projeto_id__exact=projeto_id)
    listaProjetos = projeto.objects.all()
    meuProjeto = projeto.objects.get(pk=projeto_id)
    meuProjetoNome = meuProjeto.nomeProjeto + ' - '

    c = Context({
                 'listaCasoTestes': listaCasoTestes,
                 'listaProjetos' : listaProjetos,
                 'meuProjetoNome': meuProjetoNome,
                 'meuProjeto': meuProjeto,
    })

    return render_to_response('gerenciador_testes/principal.html',
                              c,
                              context_instance=RequestContext(request))

def lista_execucoes_por_projeto(request, projeto_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')

    #Coleta lista de execucoes excluindo os testes que nao tem resultado
    listaExecucoes = casoDeTesteEmProjeto.objects.filter(projeto_id=projeto_id).exclude(resultado=None)
    listaProjetos = projeto.objects.all()
    meuProjeto = projeto.objects.get(pk=projeto_id)
    for exc in listaExecucoes:
        print ('nome do projeto: ' + str(exc.projeto_id))
        print ('nome do caso de teste: ' + str(exc.casoDeTeste_id))
        print ('resultado: ' + str(exc.resultado))
        print ('data: ' + str(exc.dataExecucao))

    c = Context({
                 #'listaCasoTestes': listaCasoTestes,
                 'listaExecucoes' : listaExecucoes,
                 'listaProjetos' : listaProjetos,
                 'meuProjeto': meuProjeto,
    })

    return render_to_response('gerenciador_testes/lista_execucoes_por_projeto.html',
                              c,
                              context_instance=RequestContext(request))
    
    #return HttpResponseRedirect('/gerenciador_testes/projeto/%s/visao_geral' % (projeto_id))

def lista_todos_casos_testes(request, projeto_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')

    form_has_any_error = False
    listaCasoTestes = casoDeTeste.objects.all()
    listaProjetos = projeto.objects.all()
    meuProjeto = projeto.objects.get(pk=projeto_id)
    meuProjetoNome = False

    if request.method == 'POST':  # If the form has been submitted
        form = CasoDeTesteForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            titulo_post = form.cleaned_data['titulo']
            caminho_post = form.cleaned_data['caminhoSikuli']
            casoDeTeste_obj = casoDeTeste(titulo=titulo_post, caminhoSikuli=caminho_post)
            casoDeTeste_obj.save()
        else:
            form_has_any_error = True
    else:    
        form = CasoDeTesteForm()

    c = Context({
                 'listaCasoTestes': listaCasoTestes,
                 'listaProjetos' : listaProjetos,
                 'form': form,
                 'form_has_any_errors' : form_has_any_error,
                 'meuProjetoNome': meuProjetoNome,
                 'meuProjeto': meuProjeto,
    })
    
    return render_to_response('gerenciador_testes/principal.html',
                              c,
                              context_instance=RequestContext(request))

def lista_passos_por_caso_de_teste(request, projeto_id, casoDeTeste_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')

    listaDePassos = casoDeTestePasso.objects.filter(casoDeTeste__exact=casoDeTeste_id)
    casoTeste = casoDeTeste.objects.get(pk=casoDeTeste_id)
    listaProjetos = projeto.objects.all()
    meuProjeto = projeto.objects.get(pk=projeto_id)
    ex = None

    try:
        if 'executar' in request.GET.keys():
            ex = True
    except MultiValueDictKeyError:
        pass
    
    c = Context({
        'listaDePassos': listaDePassos,
        'casoTeste': casoTeste,
        'listaProjetos' : listaProjetos,
        'meuProjeto' : meuProjeto,
        'ex': ex,
    })
    return render_to_response('gerenciador_testes/detail.html',
                              c,
                              context_instance=RequestContext(request))

def lista_testes_para_inserir_no_projeto(request, projeto_id):
    if request.method == 'POST':
        checkbox = request.POST.getlist('checks')
        #print ("tamanho da lista: " + str(len(checkbox)))
        #for c in checkbox:
        #    print ("valor: " + c)
        #adiciona os testes no projeto
        for c in checkbox:
            print ("inserindo teste id: " + str(c))
            casoDeTesteEmProjeto_obj = casoDeTesteEmProjeto(projeto_id=projeto.objects.get(pk=projeto_id), casoDeTeste_id=casoDeTeste.objects.get(pk=c))
            casoDeTesteEmProjeto_obj.save()

    #Prepara lista de testes para o projeto
    listaCasoTestes = casoDeTeste.objects.all().exclude(casodetesteemprojeto__projeto_id__exact=projeto_id)
    meuProjeto = projeto.objects.get(pk=projeto_id)
    
    #Seta o contexto
    c = Context({
                 'listaCasoTestes': listaCasoTestes,
                 'meuProjeto': meuProjeto,
    })
    return render_to_response('gerenciador_testes/lista_testes_inserir_no_projeto.html',
                              c,
                              context_instance=RequestContext(request))

def registra_cancelar (request, projeto_id, casoDeTeste_id):
    return HttpResponseRedirect('/gerenciador_testes/projeto/%s/lista_casos_teste_por_projeto' % (projeto_id))

def registra_passou (request, projeto_id, casoDeTeste_id):
    data_atual = str(datetime.datetime.now())[:10]
    #print("time now: " + data_atual)
    casoDeTesteEmProjeto.objects.filter(projeto_id=projeto_id, casoDeTeste_id=casoDeTeste_id).update(resultado='passou', dataExecucao=data_atual)
    return HttpResponseRedirect('/gerenciador_testes/projeto/%s/lista_casos_teste_por_projeto' % (projeto_id))

def registra_falhou (request, projeto_id, casoDeTeste_id):
    data_atual = str(datetime.datetime.now())[:10]
    #print("time now: " + data_atual)
    casoDeTesteEmProjeto.objects.filter(projeto_id=projeto_id, casoDeTeste_id=casoDeTeste_id).update(resultado='falhou', dataExecucao=data_atual)
    return HttpResponseRedirect('/gerenciador_testes/projeto/%s/lista_casos_teste_por_projeto' % (projeto_id))

def registra_sikuli (request, casoDeTeste_id):
    casoTeste = casoDeTeste.objects.get(pk=casoDeTeste_id)
    sikuliPath = 'c:\\"Program Files (x86)\\Sikuli X\\Sikuli-IDE.bat" -r '
    # caminhoTesteSikuli = '"d:\\Dropbox\\My_Saved_data\\Faculdade\\TCC I\\Sikuli\\demo\\demo.sikuli"'
    caminhoTesteSikuli = casoTeste.caminhoSikuli
    subprocess.Popen(sikuliPath + caminhoTesteSikuli, shell=True)

    print ("==============sikuli===================\n")
    print (casoTeste.caminhoSikuli)
    print (sikuliPath + caminhoTesteSikuli)
    return HttpResponseRedirect('/gerenciador_testes/1/?executar')

def remover_do_projeto(request, projeto_id, casoDeTeste_id):
    casoDeTesteEmProjeto.objects.filter(projeto_id=projeto_id, casoDeTeste_id=casoDeTeste_id).delete()
    return HttpResponseRedirect('/gerenciador_testes/projeto/%s/lista_casos_teste_por_projeto' % (projeto_id))

def remover_teste(request, projeto_id, casoDeTeste_id):
    #Remove os passos associado ao caso de teste
    casoDeTestePasso.objects.filter(casoDeTeste__exact=casoDeTeste_id).delete()

    #Remove do Projeto
    casoDeTesteEmProjeto.objects.filter(casoDeTeste_id=casoDeTeste_id).delete()

    #Remove o caso de teste
    casoDeTeste.objects.get(pk=casoDeTeste_id).delete()

    return HttpResponseRedirect('/gerenciador_testes/projeto/%s/casos_de_testes' % (projeto_id))

def visao_geral(request, projeto_id=1):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')

    meuProjeto = projeto.objects.get(pk=projeto_id)
    listaProjetos = projeto.objects.all()
    totalProjetos = len(listaProjetos)
    totalTesteEmProjeto = casoDeTeste.objects.filter(casodetesteemprojeto__projeto_id__exact=projeto_id).count()
    ultimaExecucao = 'falhou'
    acumuladoFalhas = '5.7%'
    acumuladoSucesso = '94.3%'

    c = Context({
                 'meuProjeto': meuProjeto,
                 'listaProjetos': listaProjetos,
                 'totalProjetos': totalProjetos,
                 'totalTesteEmProjeto': totalTesteEmProjeto,
                 'ultimaExecucao' : ultimaExecucao,
                 'acumuladoFalhas': acumuladoFalhas,
                 'acumuladoSucesso': acumuladoSucesso,
    })
    return render_to_response('gerenciador_testes/visao_geral.html',
                              c,
                              context_instance=RequestContext(request))