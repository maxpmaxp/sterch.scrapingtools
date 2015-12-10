### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012-2015
#######################################################################

""" Page downloading tools
"""
__author__  = "Polscha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

import logging
from config import MAXREADTRIES, DELAY
from cookielib import CookieJar
from copy import copy
from cStringIO import StringIO
from gzip import GzipFile
from handlers import BindableHTTPHandlerFactory
from interfaces import IHTTPHeadersFactory, IProxyFactory, IIPFactory, IClient
from random import randint
from time import sleep
from urlparse import urlparse
from zope.component import getUtility, ComponentLookupError
from zope.interface import directlyProvides, implements

import mimetypes
import ssl
import urllib
import urllib2 

class HTTPResponse(object):
    """ Sufficient reponse information """
    def __init__(self, **kwargs):
        self.code = kwargs.get('resp_code')
        self.content = kwargs.get('raw_content')
        self.headers = kwargs.get('resp_headers')
        self.real_url = kwargs.get('real_url')

class ClientError(Exception):
    """ Generic cleint's exception """

cjar = CookieJar()

def getproxy():
    """ Simple proxy factory """
    return None

directlyProvides(getproxy, IProxyFactory)

def getip():
    """ Simple ip factory """
    return None

directlyProvides(getip, IIPFactory)
    
def createOpener(cookies=None, headers=None, _proxies=None, debug=False, custom_handlers=None):
    handlers = [] if not debug else [urllib2.HTTPHandler(debuglevel=1),]
    if custom_handlers: handlers.extend(custom_handlers)
    if _proxies:
        proxy_support = urllib2.ProxyHandler(_proxies)
        handlers.append(proxy_support)
    
    try:
        bindip = getUtility(IIPFactory)()
        if bindip: handlers.append(BindableHTTPHandlerFactory(bindip))
    except ComponentLookupError:
        pass
    
    if cookies is not None :
        c = urllib2.HTTPCookieProcessor()
        c.cookiejar = cookies
        handlers.append(c)
    
    opener = urllib2.build_opener(*handlers)
         
    if headers:
        opener.addheaders = headers
    else:
        try:
            opener.addheaders = getUtility(IHTTPHeadersFactory)()
        except ComponentLookupError:
            pass
    return opener


def encode_multipart_formdata(fields, files):
    """
    fields is a sequence of (name, value) elements for regular form fields.
    files is a sequence of (name, filename, value) elements for data to be uploaded as files
    Return (content_type, body) ready for httplib.HTTP instance
    """
    BOUNDARY = '----------ThIs_Is_tHe_bouNdaRY_$'
    CRLF = '\r\n'
    L = []
    for (key, value) in fields:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"' % key)
        L.append('')
        L.append(value)
    for (key, filename, value) in files:
        L.append('--' + BOUNDARY)
        L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
        L.append('Content-Type: %s' % get_content_type(filename))
        L.append('')
        L.append(value)
    L.append('--' + BOUNDARY + '--')
    L.append('')
    body = CRLF.join(L)
    content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
    return content_type, body

def get_content_type(filename):
    """ Determines content type of the file """
    return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

class Client(object):
    """ Simple browser emulator implements following policy:
        every read uses same cookiejar, same proxy and same browser headers.
    """
    implements(IClient)
    delay = DELAY
    maxreadtries = MAXREADTRIES
    rotate_proxies = False
    
    def __init__(self, cookies=None, headers=None, _proxies=None, noproxy=False, x_proxy_session=False, debug=False,
                 custom_handlers=None, socket_timeout=15):
        self.resp_code = None
        self.raw_response = None
        self.resp_headers = None
        self.real_url = None
        self.debug = debug
        self.custom_handlers = custom_handlers or []
        https_handler = next((h for h in self.custom_handlers if isinstance(h, urllib2.HTTPSHandler)), None)
        if not https_handler:
            self.custom_handlers.append(urllib2.HTTPSHandler(context=ssl._create_unverified_context()))

        if cookies is not None:
            self.cookies = cookies
        else:
            self.cookies = CookieJar()
        if headers:
            self.headers = headers 
        else:
            try:
                self.headers = getUtility(IHTTPHeadersFactory)()
            except ComponentLookupError:
                self.headers = []
        if x_proxy_session:
            self.headers.append(('X-Proxy-Session', str(randint(0,10**10))))
        if not noproxy: 
            self.proxies = _proxies if _proxies else self.get_proxy()
        else:
            self.proxies = None
        self.lastURL = None
        self.socket_timeout = socket_timeout

    @staticmethod
    def get_proxy():
        try:
            p = getUtility(IProxyFactory)()
        except ComponentLookupError:
            p = None
        return {'http': p, 'https': p} if p else None

    def readpage(self, url, data=None, extra_headers=None):
        ntries = 0
        downloaded = False
        c = self.cookies
        headers = self.headers + extra_headers if extra_headers else self.headers
        opener = createOpener(cookies=c,
                              headers=headers,
                              _proxies=self.proxies,
                              debug=self.debug,
                              custom_handlers=self.custom_handlers)
        exc = ClientError("Download failed for unknown reason")
        while not downloaded and ntries < self.maxreadtries:
            try:
                topost = urllib.urlencode(data) if type(data) is dict else data
                request = urllib2.Request(url, topost, dict(headers)) if headers else urllib2.Request(url, topost)
                f = opener.open(request, timeout=self.socket_timeout)
                resp = HTTPResponse()
                resp.content = f.read()
                resp.real_url = f.geturl()
                resp.code = f.code
                resp.headers = f.headers.items() if f.headers else []
                f.close()
                downloaded = True
                opener.close()
            except Exception, ex:
                exc = ex
                scheme, netloc, path, params, query, fragment = urlparse(url)
                errinfo = "attempt=%s proxy=%s protocol=%s domain=%s url=%s request=%s headers=\"%s\"" % \
                            (ntries, self.proxies.get(scheme) if self.proxies else None, scheme, netloc, url, topost, headers)
                if type(ex) == urllib2.HTTPError:
                    logging.exception("error=HTTPError code=%d %s" % (ex.code, errinfo))
                else:
                    logging.exception("error=ConnectionError %s" % errinfo)
                opener.close()
                sleep(self.delay)
                ntries += 1
                if self.rotate_proxies:
                    self.proxies = self.get_proxy()
                opener = createOpener(cookies=c, headers=headers, _proxies=self.proxies, debug=self.debug)

        if not downloaded:
            scheme, netloc, path, params, query, fragment = urlparse(url)
            errinfo = "attempt=%s proxy=%s protocol=%s domain=%s url=%s request=%s headers=\"%s\"" % \
                        (ntries, self.proxies.get(scheme) if self.proxies else None, scheme, netloc, url, topost, headers)
            logging.exception("error=DownloadError %s" % errinfo)
            raise exc

        self.real_url = self.lastURL = resp.real_url
        self.resp_code = resp.code
        self.raw_response = page = resp.content
        self.resp_headers = resp.headers

        try:
            page = GzipFile(fileobj=StringIO(page)).read()
        except Exception:
            pass
        return page
    
    def getrealurl(self, url, extra_headers=None):
        """ returns real url after redirects """
        opener = createOpener(cookies=self.cookies,
                              headers=self.headers + extra_headers if extra_headers else self.headers,
                              _proxies=self.proxies,
                              debug=self.debug)
        
        f = opener.open(url, timeout=self.socket_timeout)
        realURL = f.geturl()
        f.close()
        return realURL

    def post_multipart(self, url, fields, files, extra_headers=None):
        """
        Post fields and files to an http host as multipart/form-data.
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return the server's response page.
        """
        content_type, body = encode_multipart_formdata(fields, files)
        global cjar 
        ntries = 0
        downloaded = False
        c = self.cookies 
        if self.cookies is not None:
            c = self.cookies
        else:
            c = cjar
        opener = createOpener(cookies=c, 
                              headers=self.headers + extra_headers if extra_headers else self.headers, 
                              _proxies=self.proxies,
                              debug=self.debug)
        content_length = str(len(body))
        headers = {'Content-Type': content_type,
                   'Content-Length': content_length}
        request = urllib2.Request(url, body, headers)
        exc = ClientError("Download failed for unknown reason")
        
        while not downloaded and ntries < MAXREADTRIES:     
            try:     
                f = opener.open(request, timeout=self.socket_timeout)
                self.raw_response = page = f.read()
                self.real_url = self.lastURL = f.geturl()
                self.resp_code = f.code
                self.resp_headers = f.headers.items() if f.headers else []
                f.close()
                downloaded = True
                opener.close()
            except Exception, ex:
                exc = ex
                scheme, netloc, path, params, query, fragment = urlparse(url)
                errinfo = "attempt=%s proxy=%s protocol=%s domain=%s url=%s contentlength=%s headers=\"%s\"" % \
                            (ntries, self.proxies.get(scheme) if self.proxies else None, scheme, netloc, url, content_length, headers)
                if type(ex) == urllib2.HTTPError:
                    logging.exception("error=HTTPError code=%d %s" % (ex.code, errinfo))
                else:
                    logging.exception("error=ConnectionError %s" % errinfo)

                opener.close()
                sleep(self.delay)
                ntries += 1
                if self.rotate_proxies:
                    self.proxies = self.get_proxy()
                opener = createOpener(cookies=c, 
                                      headers=self.headers + extra_headers if extra_headers else self.headers, 
                                      _proxies=self.proxies,
                                      debug=self.debug)
        
        if not downloaded : 
            scheme, netloc, path, params, query, fragment = urlparse(url)
            errinfo = "attempt=%s proxy=%s protocol=%s domain=%s url=%s request=%s headers=\"%s\"" % \
                        (ntries, self.proxies.get(scheme) if self.proxies else None, scheme, netloc, url, content_length, headers)
            logging.exception("error=DownloadError %s" % errinfo)
            raise exc
        try:
            page = GzipFile(fileobj=StringIO(page)).read()
        except Exception:
            pass
        return page


def clone_client(c):
    """ Completely copies client and its states """
    clone = copy(c)
    if hasattr(c, 'asp_state'):
        clone.asp_state = copy(c.asp_state)
    clone.cookies = copy(c.cookies)
    clone.proxies = copy(c.proxies)
    clone.headers = copy(c.headers)
    clone.lastURL = c.lastURL
    directlyProvides(clone, IClient)
    return clone
