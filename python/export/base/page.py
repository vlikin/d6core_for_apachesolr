import urllib2
import logging
import json
from try_do import TryDo  

class Page(TryDo):
	headers = {
		"User-Agent": "Opera/9.64 (Windows NT 5.1; U; en) Presto/2.1.1",
		"Accept": "text/html, application/xml;q=0.9, application/xhtml+xml, image/ png, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1",
		"Accept-Language": "ru,uk-UA;q=0.9,uk;q=0.8,en;q=0.7",
		"Accept-Charset": "iso-8859-1, utf-8, utf-16, *;q=0.1",
		"Accept-Encoding": "identity, *;q=0",
		"Connection": "Keep-Alive"
	}
	base_url = ""
	logger_level = logging.DEBUG
	html = ""
	data = []
	pathes = ()
	
	def LoadFromFile(self, path):
		self.logger.info("Loading data from the file - %s" % path)
		try:
			file = open(path, "r")
			self.data = json.load(file)
			file.close()
		except:
			self.logger.exception("File - %s is not loaded." % path)
			return False
		return True
		
	def SaveToFile(self, path):
		self.logger.info("Saving data to the file - %s" % path)
		try:
			file = open(path, "w")
			json.dump(self.data, file)
			file.close()
		except:
			self.logger.exception("File - %s is not saved." % path)
			return False
		return True
	
	def __init__(self, logger_name = "page_loader"):
		TryDo.__init__(self)
		self.logger = logging.getLogger(logger_name)
		self.logger.setLevel(self.logger_level)
		
	def _load(self, url, headers):
		request = urllib2.Request(url = url, headers = headers)
		file = urllib2.urlopen(url=request)
		data = file.read()
		file.close()
		return data
	
	def Load(self, url, encoding = "UTF-8"):
		self.logger.info("Loading data from the url - %s" % url)
		try:
			self.data = self._load(url, self.headers)
		except:
			self.logger.exception("Could not load from url - %s" % url)
			return None
		self.data = self.data.decode(encoding, "replace")
		return self.data
				
	def GetData(self, url):
		try:
			self.url = url
			self.html = self.Load(self.url)
			self.data = self.get_data(self.html, self.pathes)
			return self.data
		except:
			self.logger.exception("Undefined error while getting data.")
	
	def get_data(self, html, pathes):
		return