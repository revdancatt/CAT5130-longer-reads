#!/usr/bin/env python
from google.appengine.api.labs import taskqueue
from google.appengine.api import urlfetch
from google.appengine.ext import db
from django.utils import simplejson

from admin.models import Items

import os
import sys
import logging

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







################################################################################
################################################################################
#
# End of messy include stuff
#
################################################################################
################################################################################

#
# Go grab the data from the secret URL that keeps track of long stories
#
fetch_url = passwords.longreadsUrl()
result = urlfetch.fetch(url=fetch_url)

#
# If something went wrong, bail out
#
if result.status_code != 200:
  logging.debug('Fetch Fail: Something went wrong while fetching initial data URL')
  sys.exit()

#
# Try and convert the content to jsons, if that
# fails bail out.
# 
try:
  json = simplejson.loads(result.content)
except Exception:
  logging.debug('Fetch Fail: when converting initial data URL to json')
  sys.exit()
  

#
# Assume the json is the *right* format, this should be more robust, but as
# I also control the json that's getting sent I'll let it slide for the moment.
# Loop thru each one getting the API url, and checking to see if we
# already have it
#
for row in json['zeitgeist']:
  
  # Make the db call to see if we already have it 
  rows = db.GqlQuery("SELECT * FROM Items WHERE apiUrl = :1", row['apiUrl'])
  
  # if not, go grab the fill json for it
  if rows.count() == 0:
    new_fetch_url = row['apiUrl'] + '?format=json&show-fields=all&show-tags=all&api-key=' + passwords.guardian_api_key()
    new_result = urlfetch.fetch(url=new_fetch_url)
    if new_result.status_code != 200:
      logging.debug('Fetch Fail: minor: when fetching gu api')
      continue
    try:
      new_json = simplejson.loads(new_result.content)
    except Exception:
      logging.debug('Fetch Fail: minor: when converting gu api fetch to json')
      continue
    
    #
    # Now put the data so that we have something to review (I assume)
    #
    try:
      new_row                  = Items()
      new_row.apiUrl           = str(row['apiUrl'])                    
      new_row.json             = simplejson.dumps(new_json)
      new_row.view_count       = int(row['view_count'])                    
      new_row.percent          = int(row['percent'])                    
      new_row.time_spent       = float(row['time_spent'])                    
      new_row.put()
    except Exception:
      logging.debug('Fetch Fail: minor: when putting data into database')
