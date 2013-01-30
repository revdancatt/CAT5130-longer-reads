#!/usr/bin/env python
import admin.setup_django_version

from google.appengine.ext import db
from django.utils import simplejson

from admin.models import Items
import os


#
# Now I want to know what articles are waiting to be reviewed and so on
#

args = {}
args_a = os.environ['QUERY_STRING'].split('?')[0]
if len(args_a) > 0:
    args_a = args_a.split('&')
    for arg in args_a:
        value_pair = arg.split('=')
        if len(value_pair) > 0:
            args[value_pair[0]] = value_pair[1]

if 'page' in args:
    page = int(args['page'])
else:
    page = 1

rows = Items.all()
rows.filter('published = ', 1)
rows.filter('queued = ', 0)
rows.order('-published_ordinal')

rows = db.GqlQuery("SELECT * FROM Items WHERE published = 1 AND queued = 0 ORDER BY published_ordinal DESC LIMIT 20")

pagesize = 50
offset = (page - 1) * pagesize
counter = 1
winning = []

print ''
for row in rows.run(limit=pagesize, offset=offset):
    JSON = simplejson.loads(row.json)
    result = JSON['response']['content']
    try:
        print '%s - %s - <a href="%s">%s</a><br />' % (result['webPublicationDate'].split('T')[0], result['id'].split('/')[0], result['webUrl'], result['webTitle'])
    except:
        counter += 1

print '<hr />'

if page == 1:
    print '<a href="/getPublished?page=2">Page 2</a>'
else:
    print '<a href="/getPublished?page=%s">Page %s</a> | <a href="/getPublished?page=%s">Page %s</a>' % (page - 1, page - 1, page + 1, page + 1)

print '<hr />'
