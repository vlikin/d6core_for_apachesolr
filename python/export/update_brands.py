#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import simplejson
from time import sleep
from lxml.html import document_fromstring

from base.page import Page
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')

def get_content(keys):
  '''
    - It gets the random content from the google search engine
  '''
  params = urllib.urlencode({
    'q': keys,
    'v': '1.0',
    'userip': 'vlikin.blogspot.com',
    "hl" : "ru"
  })
  
  url = 'https://ajax.googleapis.com/ajax/services/search/web?%s' % params

  request = urllib2.Request(url, None, {'Referer': 'http://vlikin.blogspot.com'})
  response = urllib2.urlopen(request)

  # Process the JSON string.
  results = simplejson.load(response)
  content = ''
  for item in results['responseData']['results']:
    content = '%s -- %s' % (content, item['content'])
  return content

# It Loads the parsed data.
page = Page()
page.LoadFromFile("./data/goods_by_brand.json")

# It tries to go over the brand and generates content.
i = 0
for key, brand in page.data.iteritems():
  try:
    if brand['body'] != 'error':
      print "%d - %s" % (i, brand['title'])
      query = unicode("парфюмерия", "utf-8")
      query = ('%s -- %s' % (query, brand['title'])).encode('koi8-r')
      brand['body'] = get_content( query)
      brand["body"] = document_fromstring(brand["body"]).text_content()      
      sleep(1);
  except Exception, m:
    brand['body'] = 'error'
  i = i + 1

# It saves changes.
page.SaveToFile("./data/goods_by_brand.json")
