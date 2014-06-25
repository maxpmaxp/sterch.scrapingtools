### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012
#######################################################################

""" Captcha resolving tools with the help of http://decapthcer.com/
"""
__author__  = "Polscha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

from opener import Client

class DecaptcherException(Exception):
    """ Captcha was not solved """

def decaptcher_solve(username, password, captcha, filename=None, client=None, pict_type='0', service_url="http://poster.de-captcher.com/"):
    """ capthca --- value of capthca to solve """
    if not client:
        c = Client(noproxy=True)
    else: 
        c = client
    url = service_url
    if not filename:
        fname = "captcha"
    else:
        fname = "filename"
    fields = {'function':'picture2', 'username':username, 'password':password, 'pict_to':'0', 'pict_type':pict_type, 'submit':'Send'}
    resolved = c.post_multipart(url, fields.items(), [('pict',fname, captcha)])
    result_code = resolved.split("|")[0]
    if result_code == "0":
        return resolved.split("|")[-1]
    raise DecaptcherException("Decaptcher return code: %s" % result_code)