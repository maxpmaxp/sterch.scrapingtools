### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012, 2013
#######################################################################

"""Interfaces for the ZCA based sterch.scrapingtools package

"""
__author__  = "Polscha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

from zope.interface import Interface
from zope.component.interfaces import IFactory
from zope.schema import Int, Float, TextLine

class IConfig(Interface):
    """ Base config class """

class IHTTPHeadersFactory(IFactory):
    """ Factory of HTTP headers. See .headers.getheaders to find out format """

class IProxyFactory(IFactory):
    """ Factory of HTTP proxies. See .opener.getproxy to find out format """

class IIPFactory(IFactory):
    """ Factory of IP addresses to bind proxies. See .opener.getip to find out format """
    
class IClient(Interface):
    """ HTTP/HTTPS client interface """
    delay = Float(title=u"Delay between requests", required=True, default=0.0)
    maxreadtries = Int(title=u"Max read attempts", required=True, default=2)
    lastURL = TextLine(title=u"Last URL visited", required=False)
    
    def readpage(url, data=None, extra_headers=None):
        """ Reads data from the URL given using adding extra_headers to the request """

    def getrealurl(url, extra_headers=None):
        """ Returns real url after possible redirects adding extra_headers to the request """
    
    def post_multipart(url, fields, files, extra_headers=None):
        """
        Post fields and files to an http(s) host as multipart/form-data.
        fields is a sequence of (name, value) elements for regular form fields.
        files is a sequence of (name, filename, value) elements for data to be uploaded as files
        Return the server's response page.
        """
        
class IClientFactory(IFactory):
    """ Interface for factories produces objects of IClient interface """