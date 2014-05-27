#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf.urls import *
from django.views.decorators.cache import cache_page

urlpatterns = patterns('node.views',
	url(r'^script/(.+)/(.+)/(.+)/$', 'script'),
    url(r'^gethtml/(.+)/$', 'gethtml'),
    url(r'^importkeyword/(.+)/$', 'importKeyword'),
    url(r'^exportkeyword/(.+)/$', 'exportKeyword'),
    url(r'^switch/([\s\S]*)/url/(.+)/$', 'switch'),
    url(r'^taobao/(.+)/(.+)/$', 'taobao'),
    url(r'^amazon/(.+)/(.+)/$', 'amazon'),
    url(r'^$', 'index'),
)
