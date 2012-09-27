#!/usr/local/bin/python
# -*- coding: utf-8 -*-

from drupal.file import drupal_services_import
from base.page import Page
import pprint
import logging
from lxml.html import document_fromstring
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')

pp = pprint.PrettyPrinter()
services_url = "http://d6.viktor-skelia/services"
username = "admin"
password = "admin"
services = drupal_services_import(services_url, username, password, proxy = None)
page = Page()
page.LoadFromFile("./data/goods_by_brand.json")

for key, brand in page.data.iteritems():
  if brand["category"] == u"Мужская парфюмерия":
    brand['tid'] = 1
  elif brand["category"] == u"Женская парфюмерия":
    brand['tid'] = 2
    answer = services.create_brand(brand)
    brand["nid"] = answer["nid"]
page.SaveToFile("./data/drupal_categories.json")
quit()
