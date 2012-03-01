#!/usr/bin/python2.5
# coding=UTF-8
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

"""JSON helper application view controller."""

__author__ = 'erichiggins@google.com (Eric Higgins)'


import appengine_config  # pylint: disable-msg=C6203
try:
  import simplejson as json  # pylint: disable-msg=C6204
except ImportError:
  import json  # pylint: disable-msg=C6204
from google.appengine.api import memcache
from google.appengine.api import urlfetch
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp import util
import drjson


class IndexView(webapp.RequestHandler):
  """Main page handler."""

  def get(self):  # pylint: disable-msg=C6409
    """Show index page."""
    # Display a dark theme instead of burning retinas.
    dark = bool(self.request.get('dark', False))
    template_values = {
        'dark': dark,
    }
    rendered_page = template.render('templates/index.html', template_values)
    self.response.out.write(rendered_page)


class DrJsonView(webapp.RequestHandler):
  """JSON view handler."""

  def get(self):  # pylint: disable-msg=C6409
    """Show rendered JSON."""
    # Grab the params.
    url = self.request.get('url')
    full = bool(self.request.get('full', False))
    example = bool(self.request.get('ex', False))
    # Display a dark theme instead of burning retinas.
    dark = bool(self.request.get('dark', False))
    try:
      indent = int(self.request.get('in', 2))
    except ValueError:
      indent = 2

    # Validate the url value.
    if not url or not url.startswith(u'http'):
      return self.error(500)

    content = memcache.get(url)
    if not content:
      # Fetch the URL, make sure it's JSON.
      result = urlfetch.fetch(url)
      if result.status_code == 200:
        content = result.content
        memcache.set(url, content, time=appengine_config.URL_CACHE_TIME)
    # Load the JSON.
    try:
      structure = json.loads(content)
    except ValueError:
      return self.error(500)
    if not full:  # Print just the structure.
      structure = drjson.Process(structure, example=example)
    template_values = {
        'url': url,
        'dark': dark,
        'ex': example,
        'full': full,
        'structure': json.dumps(structure, indent=indent),
    }
    rendered_page = template.render('templates/index.html', template_values)
    self.response.out.write(rendered_page)


application = webapp.WSGIApplication([
    ('/', IndexView),
    ('/render', DrJsonView),
    ], debug=appengine_config.DEBUG)


def main():
  util.run_wsgi_app(application)


if __name__ == '__main__':
  main()
