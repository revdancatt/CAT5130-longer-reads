import admin.setup_django_version

#!/usr/bin/env python

################################################################################
#
# Add your API keys here and rename this file to passwords.py
#
################################################################################

# This is the endpoint that gives you long read stories to pick from in
# a JSON format that matches the output of the guardian API
def longreadsUrl():
  return 'http://your-endpoint-here'

def guardian_api_key():
  return 'api-key-used-for-fetching-data'

def guardian_api_key_publishing():
  return 'api-key-used-for-publishing-data' #<-- for most cases the same as above

def wordpress():
  return {
    'server': '',
    'username': '',
    'password': ''
  }
  
def twitter():
  return {
    'consumer_key': '',
    'consumer_secret': '',
    'access_token_key': '',
    'access_token_secret': ''
  }
