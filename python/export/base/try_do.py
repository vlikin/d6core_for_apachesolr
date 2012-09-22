from lxml.html import etree
import re
class TryDo:
    def __init__(self):
        return
    
    def try_xpath(self, dom_item, path):
        try:
            result = dom_item.xpath(path)
            if len(result) == 1:
                return result[0] 
        except Exception:    
            self.logger.error("Wrong XPath - %s" % path)
            return None
        
    def get_xpath_text(self, dom_item, path):
        try:
            result = dom_item.xpath(path)
            if len(result) == 1:
                result = result[0]
            etree.tostring(result)
            return etree.tostring(result) 
        except Exception, e:    
            print e
            self.logger.error("Wrong XPath - %s" % path)
            return None

    def try_search(self, pattern, str):
        try:
            me =re.search(pattern, str)
            return me.groupdict()
        except:
            self.logger.exception("Could not find the data according to the pattern - %s" % pattern)
            return None
        