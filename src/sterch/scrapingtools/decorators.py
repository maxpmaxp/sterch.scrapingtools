### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2008
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2008
#######################################################################
# $Id: decorators.py 14755 2010-05-26 12:12:56Z maxp $
#######################################################################

""" useful decorators

$Id: decorators.py 14755 2010-05-26 12:12:56Z maxp $
"""
__author__  = "Polscha Maxim (maxp@sterch.net)"
__license__ = "<undefined>" # необходимо согласование
__version__ = "$Revision: 14755 $"
__date__ = "$Date: 2010-05-26 15:12:56 +0300 (Ср, 26 май 2010) $"

def synchronized(lock):
    """ Synchronization decorator. """

    def wrap(f):
        def new_function(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return new_function
    return wrap