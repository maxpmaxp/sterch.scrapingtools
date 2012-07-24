### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012
#######################################################################

""" Page downloading tools
"""
__author__  = "Polscha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

from config import MAXREADTRIES, DELAY
from cookielib import CookieJar
from gzip import GzipFile
from handlers import BindableHTTPHandlerFactory
from interfaces import IHTTPHeadersFactory, IProxyFactory, IIPFactory
from random import choice
from time import sleep
from zope.component import getUtility, ComponentLookupError
from zope.interface import directlyProvides

import mimetypes
import os.path
import urllib
import urllib2 

cjar = CookieJar()

def getproxy():
    """ Simple proxy factory """
    return None

directlyProvides(getproxy, IProxyFactory)

def getip():
    """ Simple ip factory """
    return None

directlyProvides(getip, IIPFactory)
    
def createOpener(cookies=None, headers=None, _proxies=None):
    handlers = []
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

def readpage(url, data=None, cookies=None, headers=None, _proxies=None, needURL=False):
    """ url --- url to read
        data --- data to be POSTed. if dictionary --- in will be encoded.
        needURL --- if set to True readpage returns tuple (data, url) where url is real reading url after redirects.
    """
    global cjar 
    ntries = 0
    downloaded = False
    c = cookies 
    if cookies is not None:
        c = cookies
    else:
        c = cjar
    opener = createOpener(cookies=c, headers=headers, _proxies = _proxies)
    realURL=''
    while not downloaded and ntries < MAXREADTRIES:
        try: 
            if type(data) is dict:
                topost = urllib.urlencode(data)
            else:
                topost = data
            request = urllib2.Request(url, topost)   
            f = opener.open(request)
            if needURL: realURL = f.geturl()
            page = f.read()
            f.close()
            downloaded = True
            opener.close()
        except Exception, ex:
            if type(ex) == urllib2.HTTPError:
                print "ERROR: Can't read %s. Error %d" % (url, ex.code)
                msg = "Error %d" % ex.code
                if needURL:
                    return (msg, url)
                else:
                    return msg
            else:
                print "ERROR: network error (%s)" % url, ex
            opener.close()
            sleep(DELAY)
            ntries += 1
            opener = createOpener(cookies=c, headers=headers, _proxies = _proxies)
            
    if not downloaded : 
        print "ERROR: Can't download page %s after %d tries. %s" % (url, ntries,ex)
        page = ""
     
    if needURL:
        return (page, realURL)
    else:
        return page

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
    def __init__(self, cookies=None, headers=None, _proxies=None, noproxy=False):
         
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
        if not noproxy: 
            if _proxies:
                self.proxies = _proxies
            else: 
                try:
                    p = getUtility(IProxyFactory)()
                    self.proxies = {'http' : p, 'https' : p } if p else None
                except ComponentLookupError:
                    self.proxies = None
        else:
            self.proxies = None
        self.lastURL = None
    
    def readpage(self, url, data=None, extra_headers=None):
        data, realurl = readpage(url, data=data, 
                        cookies = self.cookies,
                        headers = self.headers + extra_headers if extra_headers else self.headers,
                        _proxies = self.proxies,
                        needURL = True)
        self.lastURL = realurl
        try:
            data = GzipFile(fileobj=StringIO(data)).read()
        except IOError:
            pass
        return data
    
    def getrealurl(self, url, extra_headers=None):
        """ returns real url after redirects """
        opener = createOpener(cookies = self.cookies,
                    headers = self.headers + extra_headers if extra_headers else self.headers,
                    _proxies = self.proxies)
        
        f = opener.open(url)
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
                              _proxies = self.proxies)
        headers = {'Content-Type': content_type,
                   'Content-Length': str(len(body))}
        request = urllib2.Request(url, body, headers)
        
        while not downloaded and ntries < MAXREADTRIES:     
            try:     
                f = opener.open(request)
                page = f.read()
                f.close()
                downloaded = True
                opener.close()
            except Exception, ex:
                if type(ex) == urllib2.HTTPError:
                    print "ERROR: Can't read %s. Error %d" % (url, ex.code)
                else:
                    print "ERROR: network error (%s)" % url, ex
                opener.close()
                sleep(DELAY)
                ntries += 1
                opener = createOpener(cookies=c, 
                                      headers=self.headers + extra_headers if extra_headers else self.headers, 
                                      _proxies = self.proxies)
        
        if not downloaded : 
            print "ERROR: Can't download page %s after %d tries. %s" % (url, ntries,ex)
            page = ""
        try:
            page = GzipFile(fileobj=StringIO(page)).read()
        except IOError:
            pass
        return page
    
class BaseCaptchaAwareClient(Client):
    """ Base class for clients that aware to solve captcha """
    
    def captcha_required(self, page):
        """ Returns True if cpatche entry required, False otherwise.
            Accepts page content as input.
        """
        raise NotImplemented()
    
    def solve_captcha(self, page):
        """ Returns page content after captcha solving.
            Accepts page content as input.
        """
        raise NotImplemented()
    
    def readpage(self, url, data=None):
        page = super(BaseCaptchaAwareClient, self).readpage(url, data)
        if self.captcha_required(page):
            is_solved = False
            ntries = 0
            while not is_solved and ntries < MAXREADTRIES: 
                try:
                    page = self.solve_captcha(page)
                    is_solved = True
                except Exception, ex:
                    print "ERROR: captcha solving error:",  ex
                sleep(DELAY)
                ntries += 1
            if not is_solved: return ''
        return page