#!/usr/bin/python2.5
#
# Copyright 2011 Google Inc. All Rights Reserved.

"""DrJson app configuration file."""

__author__ = 'erichiggins@google.com (Eric Higgins)'


from google.appengine import dist
dist.use_library('django', '1.1')
import django
assert django.VERSION[0] >= 1, 'This Django version is too old'
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
from django.conf import settings
settings._target = None


DEBUG = False

URL_CACHE_TIME = 86400  # 1 day, in seconds.

# Django settings.
TIME_ZONE = 'UTC'
DATE_FORMAT = 'N j, Y'  # e.g. Feb. 4, 2010.
DATETIME_FORMAT = 'N j, Y, P'  # e.g. Feb. 4, 2010, 4 p.m.
