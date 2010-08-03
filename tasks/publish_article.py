#!/usr/bin/env python
from google.appengine.api.labs import taskqueue
from google.appengine.api import urlfetch
from google.appengine.ext import db
from django.utils import simplejson
from datetime import datetime
from admin.models import Items

import os
import sys
import logging
import xmlrpclib

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


# Check to see if the time is too early, if it is then
# we exit here
if datetime.now().hour <= 4:
  print 'Too early'
  sys.exit()
  
# Otherwise, see if we have already published today
o = datetime.now().toordinal()
rows = db.GqlQuery("SELECT * FROM Items WHERE published_ordinal = :1", o)

# if we have then exit here
if rows.count() > 0:
  print 'Already published'
  sys.exit()
  
# Now we need to get the next item in the queue
# If there is nothing in the queue then exit
rows = db.GqlQuery("SELECT * FROM Items WHERE queued = 1 ORDER BY last_update ASC LIMIT 1")
if rows.count() == 0:
  print 'Nothing in queue'
  sys.exit()


# So *now* we have a item we want to publish
# and the json for it
pub_row = rows[0]
json = simplejson.loads(pub_row.json)
json = json['response']['content']

#
# Set up the info we need to post to wordpress
#
wp_url = 'http://' + passwords.wordpress()['server'] + '/xmlrpc.php'
wp_username = passwords.wordpress()['username']
wp_password = passwords.wordpress()['password']
wp_blogid = 0
status_published = 1
server = xmlrpclib.ServerProxy(wp_url)

#
# Grab the titles, body content, category and tags
#
title = json['fields']['headline']
content = json['fields']['body']
categories = [json['sectionName']]
tags = []
for tag in json['tags']:
  if tag['type'] == 'keyword':
    tags.append(tag['webTitle'])


#
# Add a "first published" preable with link and date if we can
#
first_published = '<p class="pub_sub">First <a href="' + json['webUrl'] + '">published online</a>'
try:
  d = datetime.strptime(str(json['webPublicationDate'].split('+')[0].replace('T',' ')), '%Y-%m-%d %H:%M:%S')
  o_pub = d.toordinal()
  o_now = datetime.now().toordinal()
  diff = datetime.now() - d
  d = d.strftime('%A&nbsp;%d&nbsp;%B&nbsp;%Y')
  first_published += ' on ' + d + '.</p>'
except:
  first_published += '.</p>'

#
# If there's a thumbnail, then add that in here too
#
if 'thumbnail' in json['fields']:
  first_published += '<img src="' + json['fields']['thumbnail'] + '" class="lead_thumb" />'
  
#
# Mush it all together
#
content = first_published + content
data = {'title': title, 'description': content, 'categories': categories, 'mt_keywords': tags}

#
# Send it to the server
#
try:
  post_id = server.metaWeblog.newPost(wp_blogid, wp_username, wp_password, data, status_published)
except:
  print 'didnt respond fast enough, assume its done it'

#
# Mark it as published
#
pub_row.published_ordinal = o
pub_row.published = 1
pub_row.queued = 0
pub_row.put()

print 'done!'