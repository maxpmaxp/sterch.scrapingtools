### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012
#######################################################################

"""Text processing functions
"""

from threading import RLock

class DuplicateValueError(Exception):
    """ Exception to raise duplicate value error """

class SyncList(list):
    """ Synchronized list """
    def __init__(self, *args, **kwargs):
        self._lock = RLock()
        super(SyncList, self).__init__(*args, **kwargs)
        
    def __getattribute__(self,name):
        if name not in ['__len__', 'append', '__contains__', 
                        'sort', 'count', 'extend', 'index',
                        'insert', 'pop', 'reverse']:
            return list.__getattribute__(self, name)
        self._lock.acquire()
        try:
            rval = list.__getattribute__(self, name)
        except Exception, ex:
            self._lock.release()
            raise ex
        self._lock.release()
        return rval
    
    def append_unique(self, value):
        """ Appends unique value to list, otherwise raises an DuplicateValueError """
        self._lock.acquire()
        if list.__contains__(self, value):
            self._lock.release() 
            raise DuplicateValueError("Value already exists:", value)
        list.append(self, value)
        self._lock.release()       