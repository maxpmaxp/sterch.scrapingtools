### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2008
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2008
#######################################################################

""" Page downloading tools

$Id: opener.py 14239 2010-04-20 10:05:00Z maxp $
"""
__author__  = "Polscha Maxim (maxp@sterch.net)"
__license__ = "<undefined>" # необходимо согласование
__version__ = "$Revision: 14239 $"
__date__ = "$Date: 2010-04-20 13:05:00 +0300 (Вт, 20 апр 2010) $"

from config import MAXREADTRIES, DELAY
from cookielib import CookieJar
from handlers import BindableHTTPHandlerFactory
from headers import getheaders
from random import choice
from time import sleep

import mimetypes
import os.path
import urllib
import urllib2 

cjar = CookieJar()

# Load proxies
__MY__PATH__ = os.path.dirname(os.path.abspath(__file__))

try:
    f = open(os.path.join(__MY__PATH__, "proxies.txt"),"rt")
    proxies = map(lambda s:s.strip(), f.readlines())
    f.close()
    proxies = filter(lambda s:not s.startswith("#"), proxies)
except Exception, ex:
    print ex
    proxies = []

# Load available IPS
try:
    f = open(os.path.join(__MY__PATH__, "ips.txt"),"rt")
    ips = map(lambda s:s.strip(), f.readlines())
    f.close()
    ips = filter(lambda s:not s.startswith("#"), ips)
except Exception, ex:
    print ex
    ips = []

    
def createOpener(cookies=None, headers=None, _proxies=None):
    global ips
    handlers = []
    if _proxies:
        proxy_support = urllib2.ProxyHandler(_proxies)
        handlers.append(proxy_support)
    
    if ips:
        handlers.append(BindableHTTPHandlerFactory(choice(ips)))
        
    if cookies is not None :
        c = urllib2.HTTPCookieProcessor()
        c.cookiejar = cookies
        handlers.append(c)
    
    opener = urllib2.build_opener(*handlers)
    
     
    if headers:
        opener.addheaders = headers
    else:
        opener.addheaders = getheaders()
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
        global proxies
         
        if cookies is not None:
            self.cookies = cookies
        else:
            self.cookies = CookieJar()
        if headers:
            self.headers = headers 
        else:
            self.headers = getheaders()
        if not noproxy: 
            if _proxies:
                self.proxies = _proxies
            elif proxies:
                self.proxies = {'http' : choice(proxies), 'https' : choice(proxies) }
            else:
                self.proxies = None
        else:
            self.proxies = None
        self.lastURL = None
    
    def readpage(self, url, data=None):
        data, realurl = readpage(url, data=data, 
                        cookies = self.cookies,
                        headers = self.headers,
                        _proxies = self.proxies,
                        needURL = True)
        self.lastURL = realurl
        return data
    
    def getrealurl(self, url):
        """ returns real url after redirects """
        opener = createOpener(cookies = self.cookies,
                    headers = self.headers,
                    _proxies = self.proxies)
        
        f = opener.open(url)
        realURL = f.geturl()
        f.close()
        return realURL

    def post_multipart(self, url, fields, files):
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
        opener = createOpener(cookies=c, headers=self.headers, _proxies = self.proxies)
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
                opener = createOpener(cookies=c, headers=headers, _proxies = self.proxies)
        if not downloaded : 
            print "ERROR: Can't download page %s after %d tries. %s" % (url, ntries,ex)
            page = ""
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