### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2008
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2008
#######################################################################

"""Text processing functions

$Id: worker.py 14192 2010-04-17 08:44:49Z maxp $
"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "<undefined>" # необходимо согласование
__version__ = "$Revision: 14192 $"
__date__ = "$Date: 2010-04-17 11:44:49 +0300 (Сб, 17 апр 2010) $"

import cPickle
import sys
import traceback
import types
from Queue import Queue, Empty
from threading import Thread, Event
from time import sleep

def workers_group_factory(in_queue, out_queue, event, timeout, activity, size):
    """ Creates and starts group of workers. Returns list of workers """
    workers = [Worker(in_queue, out_queue, 
                      event, timeout, activity)
                        for i in xrange(0, size) ]
    map(lambda t:t.start(), workers)
    return workers

def filter_dead_workers(grp):
    """ returns list of live workers from group given """
    return filter(lambda t:t.isAlive(), grp)

class Worker(Thread):
    """ Typical worker to process elements from input queue to output queue.
        Could be stopped be setting event. 
    """
    def __init__(self, in_queue, out_queue, event, timeout=5, activity = None):
        """ 
            in_queue --- input queue
            out_queue --- output queue
            timeout --- time to wait in inqueue is empty and check evtAllDone
            event --- event to stop thread activity
            activity --- callable represents worker activity. Must accept only one argument --- item.
                        Returned value will be placed to out_queue if not None.
        """
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.timeout = timeout
        self.evtAllDone = event
        if activity:
            self.activity = activity
            
        super(Worker, self).__init__()
        
    def activity(self, item):
        raise NotImplementedError("Must be implemented in descendants.")
    
    def run(self):
        """ Worker cycle """
        while True:
            if self.evtAllDone.isSet(): return
            try:
                try:
                    item = self.in_queue.get(timeout=self.timeout)
                    result = self.activity(item)  
                    if result is not None:
                        if type(result) == list or \
                           type(result) is types.GeneratorType:
                            map(self.out_queue.put, result)
                        else:
                            self.out_queue.put(result)
                except Empty, ex:
                    pass
            except Exception, ex:
                # Thread must stop if and only if event is set
                print "Worker ERROR:" + str(ex)    
                exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
                traceback.print_exception(exceptionType, exceptionValue, exceptionTraceback, file=sys.stdout)