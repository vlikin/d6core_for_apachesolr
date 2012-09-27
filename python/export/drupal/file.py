import os, sys, os.path, time, mimetypes, xmlrpclib, base64
from drupal.drupal_client import DrupalClient
from lxml.html import document_fromstring
from lxml.html import fromstring
from lxml.html import tostring
import logging

class drupal_services_import:
  
  server = None
  url = ""
  session = None
  username = ""
  password = ""
  logger_level = logging.DEBUG
  
  def __init__(self, url, username, password, proxy = None, logger_name = "drupal_services_import"):
    self.url = url
    self.username = username
    self.password = password
    self.logger = logging.getLogger(logger_name)
    self.logger.setLevel(self.logger_level)
    self.server = DrupalClient(self.url, allow_none = True,  proxy = proxy);
    self.session = self.server.login(self.username, self.password);
    
    return
    
  #Load file from the local system. 
  def load_file(self, path):
    filename = os.path.basename(path)
    filesize = os.stat(path).st_size
    filemime = mimetypes.guess_type(path)
    file = open(path, 'rb')
    data = file.read()
    file.close()  
    return {
      "filename": filename,
      "filesize": filesize,
      "filemime": filemime,
      "data": data
    }
  
  def retrieve(self, nid):
    return self.server.node.retrieve(nid)
  
  def create_brand(self, brand):
    self.logger.info("Try to create the brand - %s" % brand["title"])
    timestamp = str(int(time.time()))
    node = {
      'type': 'brand',
      'status': 1,
      'title': brand['title'],
      'body': brand['body'],
      'uid': self.session['user']['uid'],
      'name': self.session['user']['name'],
      'changed': timestamp
    }
    nod = self.server.node.create(node)
    return self.server.node.create(node)
    
  def create_page(self, page):
    timestamp = str(int(time.time()))
    body = fromstring(unicode(page["body"]) ).text_content().encode("utf-8")
    node = {
      'type': 'page',
      'status': 1,
      'title': page['title'],
      'body': body,
      'uid': self.session['user']['uid'],
      'name': self.session['user']['name'],
      'changed': timestamp
    }
    nod = self.server.node.create(node)
    return self.server.node.create(node)


  def create_good(self, good, directory_to = "sites/d6.viktor-skelia/files/cck/product_image"):
    self.logger.info("Try to create the good - %s" % good["title"])
    #Loading the file from the local system.
    file = self.load_file(good["image_path"])
    timestamp = str(int(time.time()))
    #Prepearing the file info before sending
    obj = {
        'file': base64.b64encode(file["data"]),
        'filename': file["filename"],
        'filepath': directory_to + file["filename"],
        'filesize': file["filesize"],
        'timestamp': timestamp,
        'uid': self.session['user']['uid'],
        'filemime': file['filemime'],
    }
    #Sending the file.
    created_file_short = self.server.file.create(obj)
    #Retrieving that file from the server to get server file info.
    created_file = self.server.file.retrieve(created_file_short["fid"], False)

    #Cleaning.
    #del created_file['file']
    #Filling the node info.
    body = fromstring(unicode(good["description"]) ).text_content().encode("utf-8")
    #body = document_fromstring(good["description"].encode("utf-8")).text_content()
    #body = tostring(body, encoding="utf-8")
    print "-----------------------------------------"
    print body
    print body.__class__.__name__
    node = {
      'type': 'product',
      'status': 1,
      'title': good["title"].encode("utf-8"),
      'uid': self.session['user']['uid'],
      'name': self.session['user']['name'],
      'changed': timestamp,
      'field_product_image':[created_file],
      'field_product_price': [{"value": float(good["price"])}],
      'field_product_rate': [{"value": good["rate"]}],
      'field_product_brand': [{"nid": good["brand_nid"]}] ,
      'taxonomy': {'1' : [good["tid"]]},
      'body': body
    }
    #Creating the node
    return self.server.node.create(node)
    
    

    


    
