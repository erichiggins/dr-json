#!/usr/bin/python2.6
#
# Copyright 2011 Google Inc. All Rights Reserved.

"""One-line documentation for format_printer module.

A detailed description of format_printer.
"""

__author__ = 'erichiggins@google.com (Eric Higgins)'

import optparse
import sys
try:
  import simplejson as json
except ImportError:
  import json


FLAGS = optparse.OptionParser(usage='usage: %prog [options] filename')
FLAGS.add_option('-f', '--full',
                 action='store_true', dest='full', default=False,
                 help='pretty-print full JSON file')
FLAGS.add_option('-e', '--example',
                 action='store_true', dest='example', default=False,
                 help='print example values from data file')


def CopyStructure(obj, example=False):
  """Create a simplified mirror of a dict structure.

  Args:
    obj: Dictionary object to copy the structure of.
    example: If True, copies the first value from the object structure.
  Returns:
    A minimal dictionary object copying the structure of the original.
  """
  mirror = {}
  for k, v in obj.iteritems():
    value_type = type(v)
    if value_type == type(None):
      mirror[k] = None
    else:
      mirror[k] = value_type()
    if value_type == dict:
      mirror[k] = CopyStructure(v, example)  # Subject to recursion.
    elif value_type == list:
      if v:
        first = v[0]
        first_type = type(first)
        if first_type == dict:
          mirror[k].append(CopyStructure(first, example))
        else:
          if example:
            mirror[k].append(first)
          else:
            mirror[k].append(first_type())
    else:
      if example:
        mirror[k] = v
  return mirror


def main():
  options, args = FLAGS.parse_args()
  if not args:
    FLAGS.error('filename is required.')
  # Last argument should be a JSON filename.
  try:
    fp = open(args[-1], 'r')
  except IOError:
    return
  else:
    data = json.load(fp)
    if not options.full:
      data = CopyStructure(data, options.example)
    print json.dumps(data, indent=2)


if __name__ == '__main__':
  sys.exit(main())
