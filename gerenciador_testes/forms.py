#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
from gerenciador_testes.models import casoDeTeste, projeto
from django.forms import ModelForm
import datetime

class CasoDeTesteForm(ModelForm):
    titulo = forms.CharField(max_length=200, label=u'Título')
    caminhoSikuli = forms.CharField(max_length=200, label=u'Caminho do teste no Sikuli')

    class Meta:
        model = casoDeTeste

class ProjetoForm(ModelForm):
    nomeProjeto = forms.CharField(max_length=200, label=u'Nome')
    dataAbertura = forms.DateField(initial=datetime.date.today, label=u'Data de abertura')
    
    class Meta:
        model = projeto
