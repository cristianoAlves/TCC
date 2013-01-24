#!/usr/bin/python
# -*- coding: utf-8 -*-
from django import forms

class CasoDeTesteForm(forms.Form):
    titulo = forms.CharField(max_length=200, label=u'Título')
    caminhoSikuli = forms.CharField(max_length=200, label=u'Caminho do teste no Sikuli')