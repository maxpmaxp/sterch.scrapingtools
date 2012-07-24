### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012
#######################################################################

""" Headers dictionary
"""
__author__  = "Polscha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

from random import choice, randint
from copy import copy
import string

def getheaders():
    """ Returns random browser headers """
    app = "".join(choice(string.letters) for i in xrange(0,8))
    ver = "".join(choice(string.digits) for i in xrange(0,8))
    headers = [ ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:12.0) %s/%s Gecko/20100101 Firefox/12.0' % (app, ver)),
                ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                ('Accept-Language', 'en-us,en;q=0.5'),
                ('Accept-Encoding', 'gzip,deflate'),
                ('Connection', 'keep-alive'),
                ('Cache-Control','max-age=0')
                ]
    headers.append(("X-Forwarded-For", ".".join(map(str,[10,randint(0,253),randint(0,253),randint(1,253)]))))    
    return headers 