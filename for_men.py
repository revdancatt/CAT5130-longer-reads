#!/usr/bin/env python
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
# Setup the template values, may as well throw the guardian api
# key in there at the same time
#
template_values = {
  'guardian_api_key': passwords.guardian_api_key(),
}

#
# Now I want to know what articles are waiting to be reviewed and so on
#

rows = db.GqlQuery("SELECT * FROM Items ORDER BY last_update DESC LIMIT 200")

counter = 1
results = []
for row in rows:
  
  try:
    if row.word_count >= 1000:
      json = simplejson.loads(row.json)
  
      # Keep a flag allowing us to approve or reject some content
      reject = False
      tags_ok = False
  
      # go thru the tags making sure it's either news or a feature
      for tag in json['response']['content']['tags']:
        if tag['id'] in ['tone/features', 'tone/news']:
          tags_ok = True
  
      # go thru the tags making sure it's either news or a feature
      if tags_ok == True:
        tags_still_ok = False
        for tag in json['response']['content']['tags']:
          if tag['id'] in ['artanddesign/artanddesign', 'culture/culture', 'media/media', 'science/science', 'technology/technology', 'world/world']:
            tags_still_ok = True
  
  
      #
      # if we failed the tags test, then reject the thing
      if tags_ok == False or tags_still_ok == False:
        reject = True
  
      if 'thumbnail' not in json['response']['content']['fields']:
        reject = True
        
      if reject == False:
        result = {'word_count': row.word_count, 'hotness': row.percent, 'json': json}
        results.append(result)
        counter+=1
        if counter > 5:
          break
  except Exception:
    continue
  
print 'Content-Type: application/json; charset=UTF-8'
print ''      
print simplejson.dumps(results)