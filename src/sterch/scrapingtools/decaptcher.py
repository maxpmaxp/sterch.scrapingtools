### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2008
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2008
#######################################################################

""" Captcha resolving tools with the help of http://decapthcer.com/

$Id: decaptcher.py 14192 2010-04-17 08:44:49Z maxp $
"""
__author__  = "Polscha Maxim (maxp@sterch.net)"
__license__ = "<undefined>" # необходимо согласование
__version__ = "$Revision: 14192 $"
__date__ = "$Date: 2010-04-17 11:44:49 +0300 (Сб, 17 апр 2010) $"

from opener import Client

class DecaptcherException(Exception):
    """ Captcha was not solved """

def decaptcher_solve(username, password, captcha, filename=None, client=None):
    """ capthca --- value of capthca to solve """
    if not client:
        c = Client(noproxy=True)
    else: 
        c = client
    url = "http://poster.decaptcher.com/"
    if not filename:
        fname = "captcha"
    else:
        fname = "filename"
    fields = {'function':'picture2', 'username':username, 'password':password, 'pict_to':'0', 'pict_type':'0', 'submit':'Send'}
    resolved = c.post_multipart(url, fields.items(), [('pict',fname, captcha)])
    result_code = resolved.split("|")[0]
    if result_code == "0":
        return resolved.split("|")[-1]
    raise DecaptcherException("Decaptcher return code: %s" % result_code)