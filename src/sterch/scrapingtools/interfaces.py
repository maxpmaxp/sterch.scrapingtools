### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2011
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2011
#######################################################################

"""Interfaces for the ZCA based sterch.scrapingtools package

"""
__author__  = "Polscha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

from zope.component.interfaces import IFactory

class IHTTPHeadersFactory(IFactory):
    """ Factory of HTTP headers. See .headers.getheaders to find out format """

class IProxyFactory(IFactory):
    """ Factory of HTTP proxies. See .opener.getproxy to find out format """

class IIPFactory(IFactory):
    """ Factory of IP addresses to bind proxies. See .opener.getip to find out format """
    