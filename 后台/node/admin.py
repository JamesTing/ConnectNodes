#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.contrib import admin
from node.models import urlToHtml,productKeyword


class urlToHtmlAdmin(admin.ModelAdmin):
    """docstring for UrlToHtmlAdmin"""
    list_display = ('url', 'htmlstring', 'create_time')
    search_fields = ('url',)
    #raw_id_fields = ('output',) # 它是一个包含外键字段名称的元组，它包含的字段将被展现成`` 文本框`` ，而不再是`` 下拉框`` 。
    
class productKeywordAdmin(admin.ModelAdmin):
    """docstring for UrlToHtmlAdmin"""
    list_display = ('keyword', 'create_time')
    search_fields = ('keyword',)
    #raw_id_fields = ('output',) # 它是一个包含外键字段名称的元组，它包含的字段将被展现成`` 文本框`` ，而不再是`` 下拉框`` 。


admin.site.register(urlToHtml, urlToHtmlAdmin)
admin.site.register(productKeyword, productKeywordAdmin)