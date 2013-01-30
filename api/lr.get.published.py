#!/usr/bin/env python
import admin.setup_django_version

from google.appengine.ext import db
from django.utils import simplejson

from admin.models import Items

#
# Now I want to know what articles are waiting to be reviewed and so on
#

rows = Items.all()
rows.filter('published = ', 1)
rows.filter('queued = ', 0)
rows.order('-published_ordinal')

rows = db.GqlQuery("SELECT * FROM Items WHERE published = 1 AND queued = 0 ORDER BY published_ordinal DESC LIMIT 20")

pagesize = 20
offset = 0
counter = 1
winning = []

for row in rows.run(limit=pagesize, offset=offset):
    JSON = simplejson.loads(row.json)
    result = JSON['response']['content']
    winning.append(result)

results = {'response': {
              'status': 'ok',
              'orderBy': 'newest',
              'pageSize': rows.count(),
              'results': winning,
            }
           }

print 'Content-Type: application/json; charset=UTF-8'
print ''
print simplejson.dumps(results)
