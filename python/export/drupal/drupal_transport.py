import xmlrpclib
class  DrupalTransport(xmlrpclib.Transport):
    session = {
            "session_name": "",
            "sessid": ""
    }
  
    proxy = None
    host = ""
    def set_proxy(self, proxy):
        self.proxy = proxy

    def set_session(self, session):
        self.session = session
        
    def make_connection(self, host):
        self.host = host 
        if self.proxy != None:
            connect_to = self.proxy
        else: 
            connect_to = self.host 
        connection = xmlrpclib.Transport.make_connection(self, connect_to)
        return connection
    
    def send_request(self, connection, handler, request_body):
        xmlrpclib.Transport.send_request(self, connection, handler, request_body)
        if self.session["session_name"] != "":
            connection.putheader("Cookie", "%s=%s" % (self.session["session_name"], self.session["sessid"]))
    