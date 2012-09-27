import xmlrpclib
import logging
from drupal.drupal_transport import DrupalTransport
class DrupalClient(xmlrpclib.ServerProxy):
    proxy = None
    session = None
    logger_level = logging.DEBUG
    
    def __init__(self, uri, allow_none, proxy = None, logger_name = "DrupalClient"):
        transport = DrupalTransport()
        transport.set_proxy(proxy)
        xmlrpclib.ServerProxy.__init__(self, uri = uri, transport = transport, allow_none = allow_none)
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(self.logger_level)
    
    def login(self, username, password):
        self.logger.info("User - %s trying to login" % username)    
        session = self.user.login(username, password)
        self.set_session(session)
        return session
    
    def set_session(self, session):
        self.session = session
        self._ServerProxy__transport.set_session(self.session)
    
    def connect(self):
        self.logger.info("The client is trying to connect.")
        session = self.system.connect()
        self.set_session(session)
        return session