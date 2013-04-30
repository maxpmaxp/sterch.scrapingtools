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

class IConfig(Interface):
    """ Base config class """

class IHTTPHeadersFactory(IFactory):
    """ Factory of HTTP headers. See .headers.getheaders to find out format """

class IProxyFactory(IFactory):
    """ Factory of HTTP proxies. See .opener.getproxy to find out format """

class IIPFactory(IFactory):
    """ Factory of IP addresses to bind proxies. See .opener.getip to find out format """
    