#!/usr/bin/env python
import admin.setup_django_version

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db
from django.utils import simplejson

from admin.models import Items

import os
import sys

#
# Ok, so this is annoying and daft *but* I want to keep passwords out of github
# which isn't really a problem, but there's also one unpublished URL that I
# can't make public *yet*
#
# When that URL is public, I'll clean this up to give a developer a better way
# of adding their own Wordpress and Guardian APIs and so on.
#
try:
  import passwords
except Exception:
  print ''
  print 'application is missing the passwords file'
  sys.exit()







#
# Now I want to know what articles are waiting to be reviewed and so on
#

rows = db.GqlQuery("SELECT * FROM Items WHERE published = 1 AND queued = 0 ORDER BY published_ordinal DESC LIMIT 20")

counter = 1
winning = []

for row in rows:
  JSON = simplejson.loads(row.json)
  result = JSON['response']['content']
  winning.append(result)
  
  
results = {'response': {
              'status': 'ok',
              'orderBy': 'newest',
              'pageSize': 40,
              'results': winning,
            }
           }

print 'Content-Type: application/json; charset=UTF-8'
print ''      
print simplejson.dumps(results)