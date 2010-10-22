### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2008
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2008
#######################################################################

"""Text processing functions

$Id: queue.py 14598 2010-05-17 11:10:58Z maxp $
"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "<undefined>" # необходимо согласование
__version__ = "$Revision: 14598 $"
__date__ = "$Date: 2010-05-17 14:10:58 +0300 (Пн, 17 май 2010) $"

import cPickle
from Queue import Queue, Empty
from threading import Thread, RLock, Event
from time import sleep

def pickleQueue(queue, filename):
    """ Pickles queue as a list """
    f = open(filename,"wb")
    try:
        l = []
        while True:
            l.append(queue.get(False))
    except Empty:
        pass  
    cPickle.dump(l, f)
    f.close()
    # get back all elements
    map(queue.put, l)
    
    
def unpickleQueue(filename):
    """ Unpickles list as a queue. Returns Queue object. """
    queue = Queue()
    f = open(filename,"rb")
    l = cPickle.load(f)
    f.close()
    map(queue.put, l)
    return queue
    
def processQueue(queue, callable, maxthreads, delay):
    """ Multithreading queue processing. 
        queue --- queue of objects to process
        callable --- callable object that can process queue elements
        maxthreads --- threads limit
        delay --- delay in seconds if number of active threads exceeds limit
        
        callable will be called for every queue element as argument in separate thread
        
    """
    try:
        threads = []
        while True:
            obj = queue.get(False)
            while len(threads) >= maxthreads:
                threads = filter(lambda t:t.isAlive(), threads)
                print "Queue size is %s" % queue.qsize()
                sleep(delay)
            thrd = Thread(target=callable, args=(obj,))
            thrd.start()
            threads.append(thrd)     
    except Empty:
        # Wait for all threads
        print "All queues objects in progress. Waiting..."
        while threads:
            threads = filter(lambda t:t.isAlive(), threads)
            print "Queue size is %s" % queue.qsize()
            sleep(delay)

class DumpMixIn:
    """ Mixin dumps queue """
    
    def __init__(self, calls_limit, filename,restore_from):
        self.calls_limit = calls_limit
        self.calls_counter = 0
        self.filename = filename
        if restore_from:
            self._restore_queue(restore_from)

    def _restore_queue(self, filname):
        """ Restores queue from the file given"""
        f = open(filename,"wb")
        self.queue = cPickle.load(f)
        f.close()
    
    
    def _dump(self):
        """ dumps queue content to pickle """
        self.mutex.acquire()
        self.calls_counter +=1
        if self.calls_counter > self.calls_limit:        
            fname = "%s-%s.pickle" % (self.filename, self.calls_counter)
            f = open(fname,"wb")
            cPickle.dump(self.queue, f)
            f.close()
            self.calls_counter = 0 
        self.mutex.release()
    
class DumpingPutQueue(Queue, DumpMixIn):
    """ Queue that dumps objects to file after n put calls"""
    def __init__(self, calls_limit, filename, restore_from=None, maxsize=0):
        Queue.__init__(self, maxsize)
        DumpMixIn.__init__(self, calls_limit, filename, restore_from)
        
    def put(self, item, block=True, timeout=None):
        Queue.put(self,item, block, timeout)
        self._dump()
        
class DumpingGetQueue(Queue, DumpMixIn):
    """ Queue that dumps objects to file after n put calls"""
    def __init__(self, calls_limit, filename, restore_from=None, maxsize=0):
        Queue.__init__(self, maxsize)
        DumpMixIn.__init__(self, calls_limit, filename, restore_from)
    
    def get(self, block=True, timeout=None):
        self._dump()
        return Queue.get(self, block, timeout)

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