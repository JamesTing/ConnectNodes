#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models

class urlToHtml(models.Model):
    """docstring for HtmlString"""
    url = models.CharField(max_length=500)
    htmlstring = models.TextField()
    create_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s %s %s' % (self.url, self.htmlstring, self.create_time)

    class Meta:
        ordering = ['-create_time']
        
class productKeyword(models.Model):
    """docstring for productKeyword"""
    keyword = models.CharField(max_length=50)
    create_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return u'%s %s' % (self.keyword, self.create_time)

    class Meta:
        ordering = ['-create_time']
