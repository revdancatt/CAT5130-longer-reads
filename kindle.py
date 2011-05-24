#!/usr/bin/env python
import admin.setup_django_version

from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import webapp
from google.appengine.ext import db
from django.utils import simplejson
from datetime import date, datetime

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







################################################################################
################################################################################
#
# End of messy include stuff
#
################################################################################
################################################################################






class Main(webapp.RequestHandler):
  def get(self):

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
    rows = db.GqlQuery("SELECT * FROM Items WHERE published = 1 AND queued = 0 ORDER BY published_ordinal DESC LIMIT 14")
    
    #
    # Yes, yes I know this is dumb, so go make it better, anyway I just want this
    # crap to work, so I'm going to loop over the json, load it, shove it into
    # an array and then just dump the whole thing out again, with some
    # gnarly replacing, just to make it look nice ... I know, I know, blame
    # the older version of Django being used by App Engine, when they
    # update to something sensible *then* I'll clean this up, ok?!
    #
    json_a = []
    for row in rows:
      
      new_json = simplejson.loads(row.json)
      new_json['response']['content']['fields']['time_spent'] = (row.time_spent)
      new_json['response']['content']['fields']['view_count'] = (row.view_count)
      new_json['response']['content']['fields']['percent'] = (row.percent)
      d = date.fromordinal(row.published_ordinal)
      dow = d.strftime("%A")
      new_json['response']['content']['fields']['published_ordinal'] = (row.published_ordinal)
      new_json['response']['content']['fields']['dow'] = dow
      
      # Now I want to go thru all the tags finding out where we first published it
      publishedIn = 'The Guardian'
      for tag in new_json['response']['content']['tags']:
        if tag['type'] == 'publication':
          publishedIn = tag['webTitle']
      new_json['response']['content']['fields']['publishedIn'] = publishedIn.replace('The', 'the')
      
      # And get the publication date
      d = datetime.strptime(new_json['response']['content']['webPublicationDate'].replace('T',' ').replace('Z', '').split(' ')[0], '%Y-%m-%d')
      new_json['response']['content']['fields']['publishedOn'] = datetime.strftime(d, '%a %d %b %Y')
      new_json['response']['content']['fields']['publishedFull'] = 'First published in ' + new_json['response']['content']['fields']['publishedIn'] + ' on ' + new_json['response']['content']['fields']['publishedOn']
      new_json['response']['content']['fields']['publishedFull'] = 'First published in ' + new_json['response']['content']['sectionName'] + ' on ' + new_json['response']['content']['fields']['publishedOn']
      
      
      tagsList = []
      for tag in new_json['response']['content']['tags']:
        if tag['type'] == 'keyword':
          tagsList.append(tag['webTitle'])
      new_json['response']['content']['fields']['tagsList'] = tagsList
      

      json_a.append(new_json)
          
    json_a.reverse()
      
    template_values['published_items'] = simplejson.dumps(json_a).replace('\/','/').replace('}}}, {', '}}},\n{') # << larks!!!
    template_values['json'] = json_a
    
    

    path = os.path.join(os.path.dirname(__file__), 'templates/kindle.html')
    self.response.out.write(template.render(path, template_values))
    
    

# I have no idea what's going on here, but I seem to need to 
# match up the path bit here with what brought us here from the
# main.py file
application = webapp.WSGIApplication([('/kindle', Main)], debug=True)

    
def main():
  run_wsgi_app(application)

  
if __name__ == "__main__":
  main()
  
  
  
  
