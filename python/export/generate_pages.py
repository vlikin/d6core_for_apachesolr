#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from drupal.file import drupal_services_import
from base.page import Page
import pprint
import logging
import random
from lxml.html import document_fromstring
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')

pp = pprint.PrettyPrinter()
services_url = "http://d6.viktor-skelia/services"
username = "admin"
password = "admin"
services = drupal_services_import(services_url, username, password, proxy = None)
page = Page()
page.LoadFromFile("./data/goods_by_brand.json")


def get_content(page, brand_number, good_number):
  title = ""
  body = ""
  brand_keys = random.sample(page.data, brand_number)
  for brand_key in brand_keys:
    brand = page.data[brand_key]
    title = "%s %s" %  (title, brand["title"])
    body = "%s %s" %  (title, brand["body"])
    goods = random.sample(brand["data"], (1 if len(brand["data"]) < good_number else good_number))
    print len(brand["data"])
    for good in goods:
      title = "%s %s" %  (title, good["title"])
      body = "%s %s" %  (title, good["description"])
  
  return {
    'title': title,
    'body': body
  }
  
  
for i in range(1000):
  dpage = get_content(page, 2, 2)
  answer = services.create_page(dpage)
  print answer
