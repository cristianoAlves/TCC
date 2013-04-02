#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms
import datetime

class CasoDeTesteForm(forms.Form):
    titulo = forms.CharField(max_length=200, label=u'Título')
    caminhoSikuli = forms.CharField(max_length=200, label=u'Caminho do teste no Sikuli')
    
class ProjetoForm(forms.Form):    
    nomeProjeto = forms.CharField(max_length=200, label=u'nome')
    dataAbertura = forms.DateField(initial=datetime.date.today, label=u'Data_abertura')