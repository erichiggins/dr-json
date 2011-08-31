#!/usr/bin/python2.5
#
# Copyright 2011 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
