#!/usr/bin/env python
import admin.setup_django_version
import logging
import urllib
import sys
import os

from google.appengine.ext import db
from django.utils import simplejson
from datetime import datetime
from admin.models import Items

args = {}
args_a =os.environ['QUERY_STRING'].split('?')[0]
if len(args_a) > 0:
  args_a = args_a.split('&')
  for arg in args_a:
    value_pair = arg.split('=')
    if len(value_pair) > 0:
      args[value_pair[0]] = value_pair[1]


apiUrl = urllib.unquote(args['apiUrl'])

rows = db.GqlQuery("SELECT * FROM Items WHERE apiUrl = :1", apiUrl)
for row in rows:
  row.unreviewed = 0
  row.queued = 1
  row.last_update = datetime.now()
  row.put()

response = {'status': 'ok'}
print 'Content-Type: application/json; charset=UTF-8'
print ''
print simplejson.dumps(response)


