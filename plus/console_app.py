"""
Server-side interaction with the Googl+ APIs using an API key.

Just append the key to the URI: 'key=KEY'
"""

import os
import json
from urllib2 import urlopen
from urllib2 import quote

# Load settings
settings = json.load(
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../settings.json'), 'r')
)

API_KEY = settings['google']['api_key']

def search_people(query):
    """
    GET https://www.googleapis.com/plus/v1/people?query=QUERY&key=KEY
    """
    return urlopen('https://www.googleapis.com/plus/v1/people?query=%s&key=%s' % (quote(query), API_KEY)).read()


def search_activities(query, order_by_recent=True):
    """
    GET https://www.googleapis.com/plus/v1/activities?query=QUERY&key=KEY
    """
    return urlopen('https://www.googleapis.com/plus/v1/activities?query=%s&orderBy=%s&key=%s' %\
        (quote(query), 'recent' if order_by_recent else 'best', API_KEY)).read()


if __name__ == '__main__':
    #print search_people('gabe newell steam')
    print search_activities('#Otters')