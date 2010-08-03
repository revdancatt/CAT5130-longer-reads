#!/usr/bin/env python
from google.appengine.ext import db

class Items(db.Model):
  apiUrl            = db.StringProperty()
  json              = db.TextProperty()
  unreviewed        = db.IntegerProperty(default=1)
  rejected          = db.IntegerProperty(default=0)
  queued            = db.IntegerProperty(default=0)
  published         = db.IntegerProperty(default=0)
  published_ordinal = db.IntegerProperty(default=0)
  backfilled        = db.IntegerProperty(default=0)
  view_count        = db.IntegerProperty(default=0)
  percent           = db.IntegerProperty(default=0)
  time_spent        = db.FloatProperty(default=0.0)
  word_count        = db.IntegerProperty(default=0)
  last_update       = db.DateTimeProperty(auto_now_add=True, required=True)