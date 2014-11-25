### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012-2014
#######################################################################

"""Client classes for the Zope 3 based
"""
__author__  = """Polscha Maxim (maxp@sterch.net) 
                 Partially copy-pasted from http://code.activestate.com/recipes/456195/
                 and http://bugs.python.org/issue11220 """
__license__ = "ZPL" 

import httplib, logging, ssl, urllib2, socket

class ProxyHTTPConnection(httplib.HTTPConnection):
    _ports = {'http' : 80, 'https' : 443}

    def request(self, method, url, body=None, headers={}):
        #request is called before connect, so can interpret url and get
        #real host/port to be used to make CONNECT request to proxy
        proto, rest = urllib.splittype(url)
        if proto is None:
            raise ValueError, "unknown URL type: %s" % url
        #get host
        host, rest = urllib.splithost(rest)
        #try to get port
        host, port = urllib.splitport(host)
        #if port is not defined try to get from proto
        if port is None:
            try:
                port = self._ports[proto]
            except KeyError:
                raise ValueError, "unknown protocol for: %s" % url
        self._real_host = host
        self._real_port = port
        self._headers = headers
        httplib.HTTPConnection.request(self, method, url, body, headers)
        

    def connect(self):
        httplib.HTTPConnection.connect(self)
        #send proxy CONNECT request
        str = "CONNECT %s:%d HTTP/1.0\r\n" % (self._real_host, self._real_port)
        #str += "\r\n".join(["%s: %s" % (k,v) for k,v in self._headers.items()])
        #str += "\r\n\r\n"
        #str += "User-Agent: Wget/1.11.4\r\nConnection: close\r\nAccept: */*\r\nAccept-Encoding: identity\r\n\r\n"
        str += "User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; uk; rv:1.9.1.8) Gecko/20100202 Firefox/3.5.8 (.NET CLR 3.5.30729)\r\n"
        str += "Host: edit.yahoo.com:443\r\n\r\n"
        
        self.send(str) 
        #expect a HTTP/1.0 200 Connection established
        response = self.response_class(self.sock, strict=self.strict, method=self._method)
        (version, code, message) = response._read_status()
        #probably here we can handle auth requests...
        if code != 200:
            #proxy returned and error, abort connection, and raise exception
            self.close()
            raise socket.error, "Proxy connection failed: %d %s" % (code, message.strip())
        #eat up header block from proxy....
        while True:
            #should not use directly fp probablu
            line = response.fp.readline()
            if line == '\r\n': break

class ConnectHTTPHandler(urllib2.HTTPHandler):
    def do_open(self, http_class, req):
        return urllib2.HTTPHandler.do_open(self, ProxyHTTPConnection, req)

# Work around python build with no SSL support
try:  
    from urllib2 import HTTPSHandler
    
    class ProxyHTTPSConnection(ProxyHTTPConnection):
        default_port = 443
        
        def __init__(self, host, port = None, key_file = None, cert_file = None, strict = None):
            ProxyHTTPConnection.__init__(self, host, port)
            self.key_file = key_file
            self.cert_file = cert_file
        
        def connect(self):
            ProxyHTTPConnection.connect(self)
            #make the sock ssl-aware
            ssl = socket.ssl(self.sock, self.key_file, self.cert_file)
            self.sock = httplib.FakeSocket(self.sock, ssl)
            
    class ConnectHTTPSHandler(urllib2.HTTPSHandler):
        def do_open(self, http_class, req):
            return urllib2.HTTPSHandler.do_open(self, ProxyHTTPSConnection, req)
    
except ImportError, ex:
    logging.warning("SSL not supported")

class CustomRedirectHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(
            self, req, fp, code, msg, headers)
        result.status = code
        return result
    
class BindableHTTPConnection(httplib.HTTPConnection):
    def connect(self):
        """Connect to the host and port specified in __init__."""
        self.sock = socket.socket()
        if self.source_ip: self.sock.bind((self.source_ip, 0))
        self.sock.connect((self.host,self.port))

def BindableHTTPConnectionFactory(source_ip=None):
    def _get(host, port=None, strict=None, timeout=None):
        bhc=BindableHTTPConnection(host, port=port, strict=strict, timeout=timeout)
        bhc.source_ip=source_ip
        return bhc
    return _get

def  BindableHTTPHandlerFactory(source_ip):
    class BindableHTTPHandler(urllib2.HTTPHandler):
        def http_open(self, req):
            return self.do_open(BindableHTTPConnectionFactory(source_ip), req)
    return BindableHTTPHandler

class HTTPSConnectionV3(httplib.HTTPSConnection):
    def __init__(self, *args, **kwargs):
        httplib.HTTPSConnection.__init__(self, *args, **kwargs)
        
    def connect(self):
        sock = socket.create_connection((self.host, self.port), self.timeout)
        if self._tunnel_host:
            self.sock = sock
            self._tunnel()
        try:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv3)
        except ssl.SSLError, e:
            self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)
            
class HTTPSHandlerV3(urllib2.HTTPSHandler):
    def https_open(self, req):
        return self.do_open(HTTPSConnectionV3, req)
