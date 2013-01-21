#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models


class CasoDeTeste(models.Model):
    titulo = models.CharField(max_length=200)
    caminho_sikuli = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.titulo
    
    class Meta:
        verbose_name = u'Casos de teste'
        verbose_name_plural = u'Casos de teste'
    
class CasoDeTestePasso(models.Model):
    caso_teste = models.ForeignKey(CasoDeTeste)
    n_passo = models.IntegerField()
    desc_passos = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.desc_passos
    
    class Meta:
        verbose_name = u'Passos dos casos de testes'
        verbose_name_plural = u'Passos dos casos de testes'

class Status(models.Model):
    status = models.BooleanField()    
    
    class Meta:
        verbose_name = u'Status'
        verbose_name_plural = u'Status'
    
class Execucao(models.Model):
    caso_teste = models.ForeignKey(CasoDeTeste)
    status = models.ForeignKey(Status)
    exec_date = models.DateTimeField('data execucao')
    
    class Meta:
        verbose_name = 'Execuções'
        verbose_name_plural = 'Execuções'
