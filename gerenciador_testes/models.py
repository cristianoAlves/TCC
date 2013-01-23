#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models

class casoDeTeste(models.Model):
    titulo = models.CharField(max_length=200)
    caminhoSikuli = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.titulo
    
    class Meta:
        verbose_name = u'Casos de teste'
        verbose_name_plural = u'Casos de teste'
    
class casoDeTestePasso(models.Model):
    casoDeTeste = models.ForeignKey(casoDeTeste)
    nPasso = models.IntegerField()
    desc = models.CharField(max_length=200)
    resultExperado = models.CharField(max_length=200)
    
class Meta:
        verbose_name = u'Passos dos casos de testes'
        verbose_name_plural = u'Passos dos casos de testes'
        
class testSet(models.Model):    
    nome = models.CharField(max_length=200)
    dataAbertura = models.DateField('data de abertura')
    dataFechamento = models.DateField('data de fechamento', null=True, blank=True)
    
    def __unicode__(self):
        return self.nome
    
class casoDeTesteVsTestSet(models.Model):
    casoDeTeste = models.ForeignKey(casoDeTeste)
    testSet = models.ForeignKey(testSet)
