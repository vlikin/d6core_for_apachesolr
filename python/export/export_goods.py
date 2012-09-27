from drupal.file import drupal_services_import
from base.page import Page
import pprint
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s')

pp = pprint.PrettyPrinter()
services_url = "http://d6.viktor-skelia/services"
username = "admin"
password = "admin"
services = drupal_services_import(services_url, username, password, proxy = None)
page = Page()
page.LoadFromFile("./data/drupal_categories.json")
index = 0
for key, brand in page.data.iteritems():
    for good in brand["data"]:
        if good.has_key('sent') and  good['sent'] == True:
                print "continue ->"
                continue
        try:
          good["brand_nid"] = brand["nid"]
          good["tid"] = brand["tid"]
          good["price"] = good["price"][:-4]
          services.create_good(good)
          print "new"
          good["sent"] = True
        #print good
        except Exception as  e:
          print e
          print "error"
          good["sent"] = False
    index = index + 1
page.SaveToFile("./data/drupal_goods_last.json" )
quit()
print "End."
