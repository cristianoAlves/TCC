from django.template import Context
from django.template import RequestContext
from django.http import HttpResponseRedirect
from gerenciador_testes.models import casoDeTeste, casoDeTestePasso, projeto, casoDeTesteEmProjeto
from django.shortcuts import render_to_response
from django.contrib import auth
from forms import CasoDeTesteForm, ProjetoForm, CasoDeTestePassoForm
from django.utils.datastructures import MultiValueDictKeyError
import subprocess
import datetime



def logoutRequest(request):
    auth.logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect('/gerenciador_testes/login')

def lista_projetos(request, projeto_id=0):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')

    form_has_any_error = False
    listaProjetos = projeto.objects.all()
    meuProjeto = request.session['projetoid']
    edit = False
    
    if request.method == 'POST':  # If the form has been submitted
        formProj = ProjetoForm(request.POST)  # A form bound to the POST data
        if formProj.is_valid():  # All validation rules pass
            nome_post = formProj.cleaned_data['nomeProjeto']
            data_post = formProj.cleaned_data['dataAbertura']

            # Verifica se for um edit, caso sim(else), coleta as novas informacoes e faz um update
            if projeto_id == 0:
                projeto_obj = projeto(nomeProjeto=nome_post, dataAbertura=data_post)
                projeto_obj.save()
            else:
                projeto.objects.filter(pk=projeto_id).update(nomeProjeto=nome_post, dataAbertura=data_post)
        else:
            form_has_any_error = True 
    else:
        # Caso do edit, se nao for =0, significa que o projeto esta sendo editado,
        # neste caso, o form precisa enviar os dados do projeto para tela
        if not projeto_id == 0:
            meuProjetoEdit = projeto.objects.get(pk=projeto_id)
            formProj = ProjetoForm(instance=meuProjetoEdit)
            edit = True 
        else:
            formProj = ProjetoForm()

    c = Context({
                 'listaProjetos': listaProjetos,
                 'meuProjeto': meuProjeto,
                 'formProj': formProj,
                 'form_has_any_errors' : form_has_any_error,
                 'edit' : edit,
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

    # Coleta lista de execucoes excluindo os testes que nao tem resultado
    listaExecucoes = casoDeTesteEmProjeto.objects.filter(projeto_id=projeto_id).exclude(resultado=None)
    listaProjetos = projeto.objects.all()
    meuProjeto = projeto.objects.get(pk=projeto_id)
    for exc in listaExecucoes:
        print ('nome do projeto: ' + str(exc.projeto_id))
        print ('nome do caso de teste: ' + str(exc.casoDeTeste_id))
        print ('resultado: ' + str(exc.resultado))
        print ('data: ' + str(exc.dataExecucao))

    c = Context({
                 # 'listaCasoTestes': listaCasoTestes,
                 'listaExecucoes' : listaExecucoes,
                 'listaProjetos' : listaProjetos,
                 'meuProjeto': meuProjeto,
    })

    return render_to_response('gerenciador_testes/lista_execucoes_por_projeto.html',
                              c,
                              context_instance=RequestContext(request))

def lista_todos_casos_testes(request, projeto_id, casoDeTeste_id=0):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')

    form_has_any_error = False
    listaCasoTestes = casoDeTeste.objects.all()
    listaProjetos = projeto.objects.all()
    meuProjeto = projeto.objects.get(pk=projeto_id)
    meuProjetoNome = False
    edit = False

    if request.method == 'POST':  # If the form has been submitted
        form = CasoDeTesteForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            titulo_post = form.cleaned_data['titulo']
            caminho_post = form.cleaned_data['caminhoSikuli']

            # Verifica se for um edit, caso sim(else), coleta as novas informacoes e faz um update
            if casoDeTeste_id == 0:
                casoDeTeste_obj = casoDeTeste(titulo=titulo_post, caminhoSikuli=caminho_post)
                casoDeTeste_obj.save()
                # limpa o form
                form = CasoDeTesteForm()
                return HttpResponseRedirect('/gerenciador_testes/projeto/%s/casos_de_testes' % (projeto_id))
                
            else:
                casoDeTeste.objects.filter(pk=casoDeTeste_id).update(titulo=titulo_post, caminhoSikuli=caminho_post)
                # limpa o form
                form = CasoDeTesteForm()
                return HttpResponseRedirect('/gerenciador_testes/projeto/%s/casos_de_testes' % (projeto_id))
        else:
            form_has_any_error = True
    else:
        # Caso do edit, se nao for =0, significa que o teste esta sendo editado,
        # neste caso, o form precisa enviar os dados do caso de teste para tela
        if not casoDeTeste_id == 0:
            casoTeste = casoDeTeste.objects.get(pk=casoDeTeste_id)
            form = CasoDeTesteForm(instance=casoTeste)
            edit = True 
        else:
            form = CasoDeTesteForm()
            # return HttpResponseRedirect('/gerenciador_testes/projeto/%s/casos_de_testes' % (projeto_id))

    c = Context({
                 'listaCasoTestes': listaCasoTestes,
                 'listaProjetos' : listaProjetos,
                 'form': form,
                 'form_has_any_errors' : form_has_any_error,
                 'meuProjetoNome': meuProjetoNome,
                 'meuProjeto' : meuProjeto,
                 'edit' : edit,
    })

    return render_to_response('gerenciador_testes/principal.html',
                              c,
                              context_instance=RequestContext(request))

def lista_passos_por_caso_de_teste(request, projeto_id, casoDeTeste_id, casoDeTestePasso_id=0):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')

    form_has_any_error = False
    listaDePassos = casoDeTestePasso.objects.filter(casoDeTeste__exact=casoDeTeste_id)
    casoTeste = casoDeTeste.objects.get(pk=casoDeTeste_id)
    listaProjetos = projeto.objects.all()
    meuProjeto = projeto.objects.get(pk=projeto_id)
    ex = None
    edit = False

    try:
        if 'executar' in request.GET.keys():
            ex = True
    except MultiValueDictKeyError:
        pass
    
    if request.method == 'POST':  # If the form has been submitted
        form = CasoDeTestePassoForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            print('** form is valid **')
            descPost = form.cleaned_data['desc']
            resultPost = form.cleaned_data['resultExperado']

            # Verifica se for um edit, caso sim(else), coleta as novas informacoes e faz um update
            if casoDeTestePasso_id == 0:
                print('** casoDeTestePasso = 0 **')
                casoDeTestePasso_obj = casoDeTestePasso(casoDeTeste=casoTeste, nPasso=1, desc=descPost, resultExperado=resultPost)
                casoDeTestePasso_obj.save()
                # limpa o form
                form = CasoDeTestePassoForm()
                return HttpResponseRedirect('/gerenciador_testes/projeto/%s/casos_de_testes/%s' % (projeto_id, casoDeTeste_id))

            else:
                print('** pass **')  # casoDeTeste.objects.filter(pk=casoDeTeste_id).update(titulo=titulo_post, caminhoSikuli=caminho_post)
                # limpa o form
                # form = CasoDeTesteForm()
                # return HttpResponseRedirect('/gerenciador_testes/projeto/%s/casos_de_testes' % (projeto_id))
        else:
            print('** form has any error **')
            form_has_any_error = True
    else:
        # Caso do edit, se nao for =0, significa que o teste esta sendo editado,
        # neste caso, o form precisa enviar os dados do caso de teste para tela
        form = CasoDeTestePassoForm()  # if not casoDeTeste_id == 0:
        print('***************  aki ******************')
            # casoTeste = casoDeTeste.objects.get(pk=casoDeTeste_id)
            # form = CasoDeTesteForm(instance=casoTeste)
            # edit = True 
        # else:
         #   form = CasoDeTesteForm()
    
    
    c = Context({
        'listaDePassos': listaDePassos,
        'casoDeTeste': casoTeste,
        'listaProjetos' : listaProjetos,
        'meuProjeto' : meuProjeto,
        'ex': ex,
        'form': form,
    })
    return render_to_response('gerenciador_testes/detail.html',
                              c,
                              context_instance=RequestContext(request))

def lista_testes_para_inserir_no_projeto(request, projeto_id):
    if request.method == 'POST':
        checkbox = request.POST.getlist('checks')
        for c in checkbox:
            print ("inserindo teste id: " + str(c))
            casoDeTesteEmProjeto_obj = casoDeTesteEmProjeto(projeto_id=projeto.objects.get(pk=projeto_id), casoDeTeste_id=casoDeTeste.objects.get(pk=c))
            casoDeTesteEmProjeto_obj.save()

    # Prepara lista de testes para o projeto
    listaCasoTestes = casoDeTeste.objects.all().exclude(casodetesteemprojeto__projeto_id__exact=projeto_id)
    meuProjeto = projeto.objects.get(pk=projeto_id)

    # Seta o contexto
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
    print ('data: ' + data_atual)
    casoDeTesteEmProjeto.objects.filter(projeto_id=projeto_id, casoDeTeste_id=casoDeTeste_id).update(resultado='passou', dataExecucao=data_atual)
    return HttpResponseRedirect('/gerenciador_testes/projeto/%s/lista_casos_teste_por_projeto' % (projeto_id))

def registra_falhou (request, projeto_id, casoDeTeste_id):
    data_atual = str(datetime.datetime.now())[:10]

    casoDeTesteEmProjeto.objects.filter(projeto_id=projeto_id, casoDeTeste_id=casoDeTeste_id).update(resultado='falhou', dataExecucao=data_atual)
    return HttpResponseRedirect('/gerenciador_testes/projeto/%s/lista_casos_teste_por_projeto' % (projeto_id))

def registra_sikuli (request, projeto_id, casoDeTeste_id):
    casoTeste = casoDeTeste.objects.get(pk=casoDeTeste_id)
    sikuliPath = 'c:\\"Program Files (x86)\\Sikuli X\\Sikuli-IDE.bat" -r '
    # caminhoTesteSikuli = '"d:\\Dropbox\\My_Saved_data\\Faculdade\\TCC I\\Sikuli\\demo\\demo.sikuli"'
    caminhoTesteSikuli = casoTeste.caminhoSikuli
    subprocess.Popen(sikuliPath + caminhoTesteSikuli, shell=True)

    print ("==============sikuli===================\n")
    print (casoTeste.caminhoSikuli)
    print (sikuliPath + caminhoTesteSikuli)
    # return HttpResponseRedirect('/gerenciador_testes/1/?executar')
    return HttpResponseRedirect('/gerenciador_testes/projeto/%s/casos_de_testes/%s/?executar' % (projeto_id, casoDeTeste_id))

def remover_do_projeto(request, projeto_id, casoDeTeste_id):
    casoDeTesteEmProjeto.objects.filter(projeto_id=projeto_id, casoDeTeste_id=casoDeTeste_id).delete()
    return HttpResponseRedirect('/gerenciador_testes/projeto/%s/lista_casos_teste_por_projeto' % (projeto_id))

def remover_projeto(request, projeto_id):
    # remove todos os testes do projeto
    casoDeTesteEmProjeto.objects.filter(projeto_id=projeto_id).delete()
    
    # remove o projeto
    projeto.objects.get(pk=projeto_id).delete()

    return HttpResponseRedirect('/gerenciador_testes/projeto/')

def remover_teste(request, projeto_id, casoDeTeste_id):
    # Remove os passos associado ao caso de teste
    casoDeTestePasso.objects.filter(casoDeTeste__exact=casoDeTeste_id).delete()

    # Remove do Projeto
    casoDeTesteEmProjeto.objects.filter(casoDeTeste_id=casoDeTeste_id).delete()

    # Remove o caso de teste
    casoDeTeste.objects.get(pk=casoDeTeste_id).delete()

    return HttpResponseRedirect('/gerenciador_testes/projeto/%s/casos_de_testes' % (projeto_id))

def visao_geral(request, projeto_id=1):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/gerenciador_testes/login')
    
    

    meuProjeto = projeto.objects.get(pk=projeto_id)
    request.session['projetoid'] = meuProjeto
    
    listaProjetos = projeto.objects.all()
    totalProjetos = len(listaProjetos)
    totalTesteEmProjeto = casoDeTeste.objects.filter(casodetesteemprojeto__projeto_id__exact=projeto_id).count()

    # descobre qual status da ultima execucao
    # ultimoTesteExecutado = casoDeTesteEmProjeto.objects.filter(projeto_id=projeto_id).latest('dataExecucao')

    # Coleta dos resultados gerais
    passou = casoDeTesteEmProjeto.objects.filter(projeto_id=projeto_id, resultado__exact='passou').count()
    falhou = casoDeTesteEmProjeto.objects.filter(projeto_id=projeto_id, resultado__exact='falhou').count()
    aguardandoExecucao = casoDeTesteEmProjeto.objects.filter(projeto_id=projeto_id, resultado=None).count()
    totalTesteValidosParaExecutar = totalTesteEmProjeto - aguardandoExecucao

    if totalTesteValidosParaExecutar > 0 :
        acumuladoFalhas = str(falhou * 100 / totalTesteValidosParaExecutar)
        acumuladoSucesso = str(passou * 100 / totalTesteValidosParaExecutar)
    else:
        acumuladoFalhas = 0
        acumuladoSucesso = 0

    c = Context({
                 'meuProjeto': meuProjeto,
                 'listaProjetos': listaProjetos,
                 'totalProjetos': totalProjetos,
                 'totalTesteEmProjeto': totalTesteEmProjeto,
                 # 'ultimoTesteExecutado' : ultimoTesteExecutado,
                 'acumuladoFalhas': acumuladoFalhas,
                 'acumuladoSucesso': acumuladoSucesso,
                 'aguardandoExecucao': aguardandoExecucao,
    })
    return render_to_response('gerenciador_testes/visao_geral.html',
                              c,
                              context_instance=RequestContext(request))
