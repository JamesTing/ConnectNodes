#!/usr/bin/env python
# coding: utf-8

import os,sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'link.settings'

from django.core.handlers.wsgi import WSGIHandler
application = WSGIHandler() 
