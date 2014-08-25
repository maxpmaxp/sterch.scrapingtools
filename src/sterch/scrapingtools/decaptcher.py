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

def decaptcher_solve(username, password, captcha, filename=None, client=None, pict_type='0', service_url="http://poster.de-captcher.com/", **kwargs):
    """ capthca --- value of captcha to solve 
        kwargs - optional args to be added to request
    """
    if not client:
        c = Client(noproxy=True)
    else: 
        c = client
    url = service_url
    fname = filename or 'captcha'
    fields = {'function':'picture2', 'username':username, 'password':password, 'pict_to':'0', 'pict_type':pict_type, 'submit':'Send'}
    if kwargs: fields.update(kwargs)
    resolved = c.post_multipart(url, fields.items(), [('pict',fname, captcha)])
    result_code = resolved.split("|")[0]
    if result_code == "0":
        text = resolved.split("|")[-1]
        ut = text.upper()
        if ut: 
            for c in ("'", " "):
                while c in ut: ut = ut.replace(c, "") 
        if not ut or ut == 'UN' or any(map(lambda _:_ in ut, ('DONTSEE', 'NOSEE', 'CANTSEE', 'BLANK', 'ERROR', 'IMAGE', 'UNKNO'))): 
            raise DecaptcherException("Decaptcher returned bad response: %s" % text)
        return resolved.split("|")[-1]
    raise DecaptcherException("Decaptcher returned code: %s" % result_code)