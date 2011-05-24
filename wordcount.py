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
      'msg': 'hello world'
    }
    
    path = os.path.join(os.path.dirname(__file__), 'templates/wordcount.html')
    self.response.out.write(template.render(path, template_values))
    
    

# I have no idea what's going on here, but I seem to need to 
# match up the path bit here with what brought us here from the
# main.py file
application = webapp.WSGIApplication([('/wordcount', Main)], debug=True)

    
def main():
  run_wsgi_app(application)

  
if __name__ == "__main__":
  main()
  
  
  
  
