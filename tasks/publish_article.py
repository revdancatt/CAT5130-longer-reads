#!/usr/bin/env python
import admin.setup_django_version
import os
import sys
import logging
import xmlrpclib
import admin.twitter as twitter

from google.appengine.api.labs import taskqueue
from google.appengine.api import urlfetch
from google.appengine.ext import db
from django.utils import simplejson
from datetime import datetime
from admin.models import Items


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

print ''

# Check to see if the time is too early, if it is then
# we exit here
if datetime.now().hour <= 3:
  print 'Too early for 1st publish'
  print datetime.now().hour
  sys.exit()
  
# Otherwise, see what has already published today
o = datetime.now().toordinal()
rows = db.GqlQuery("SELECT * FROM Items WHERE published_ordinal = :1", o)

# If we have aleady published 2 articles today, then no more
if rows.count() >= 2:
  print 'Already published 2 articles'
  sys.exit()
  
# If the time is before 3pm and we have just 1 article published
# then we exit again.
#
# In theory this means that when we have 0 articles published we'll still
# get past this step, when when we get to 16:00 we'll move past this step
# to publish a second article, and then the fact we have a second article
# we kick us out in the above check
if datetime.now().hour <= 13 and rows.count() == 1:
  print 'Too early for 2nd publish'
  print datetime.now().hour
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


################################################################################
#
# Do twitter stuff first
#
################################################################################
wordCount = len(json['fields']['body'].split(' '))
webTitle = json['webTitle']
shortUrl = json['fields']['shortUrl']

if wordCount >= 1500:
  tweetTitle = '%s %s #longreads' % (webTitle, shortUrl)
  if len(tweetTitle) > 128:
    shortenBy = len(tweetTitle) - 125
    webTitle = webTitle[0:shortenBy]
    webTitle = '%s...' % webTitle
    tweetTitle = '%s %s #longreads' % (webTitle, shortUrl)
else:
  tweetTitle = '%s %s' % (webTitle, shortUrl)
  if len(tweetTitle) > 128:
    shortenBy = len(tweetTitle) - 125
    webTitle = webTitle[0:shortenBy]
    webTitle = '%s...' % webTitle
    tweetTitle = '%s %s' % (webTitle, shortUrl)
    
# Let us try and post it to twitter first...
# prepare the auth thingy
api = twitter.Api(  consumer_key=passwords.twitter()['consumer_key'],
                    consumer_secret=passwords.twitter()['consumer_secret'],
                    access_token_key=passwords.twitter()['access_token_key'],
                    access_token_secret=passwords.twitter()['access_token_secret'],
                    cache=None)

# post the status
try:
  status = api.PostUpdate(tweetTitle)
except:
  pub_row.published_ordinal = 0
  pub_row.published = 1
  pub_row.queued = 0
  pub_row.put()
  print 'failed to post!'
  sys.exit()



################################################################################
#
# Set up the info we need to post to wordpress
#
################################################################################
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
  first_published += ' on ' + d
except:
  first_published += ''

#
# If there's a thumbnail, then add that in here too
#
if 'byline' in json['fields']:
  first_published += ' by ' + json['fields']['byline']
  
first_published += '.</p>'

if 'thumbnail' in json['fields']:
  content = '<p><img src="' + json['fields']['thumbnail'] + '" class="lead_thumb" /></p>' + content

#
# Mush it all together
#
content = content + first_published
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