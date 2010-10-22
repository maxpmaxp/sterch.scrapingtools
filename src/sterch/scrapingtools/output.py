### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2008
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2008
#######################################################################

"""Output functions

$Id: output.py 14192 2010-04-17 08:44:49Z maxp $
"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "<undefined>" # необходимо согласование
__version__ = "$Revision: 14192 $"
__date__ = "$Date: 2010-04-17 11:44:49 +0300 (Сб, 17 апр 2010) $"

import cgitb
import sys
from threading import RLock

class WebOutputWriter(object):
    """ Output to webpage """

    def __init__(self, old_writer):
        self.old_writer = old_writer
        self.lock = RLock()
        
    def write(self, s=""):
        """ Prints chunck according to Transfer-Encofing: chunked specification"""
        self.lock.acquire()
        #if s:
        #    if not s.endswith("\r\n") : s = "%s\r\n" % s
        self.old_writer.write(str(hex(len(s))).upper()[2:]) # chunk size
        self.old_writer.write("\r\n")
        self.old_writer.write(s)
        self.old_writer.write("\r\n")
        #Last chunk
        if not s: self.old_writer.write("\r\n")
        self.lock.release() 

def start_chunked_stdout(contentType="text/plain"):
    """ Redefines standart output to be chuncked """
    cgitb.enable()
    print "Content-Type: %s" % contentType     # HTML is following
    print 'Cache-Control: no-cache'
    print 'Expires: -1'
    print 'Pragma: no-cache'
    print "Transfer-Encoding: chunked"  # chuncked content
    print                               # blank line, end of headers
    sys.stdout = WebOutputWriter(sys.stdout)
    
def stop_chunked_stdout():
    """ Stops chunked stdout """
    sys.stdout = sys.stdout.old_writer
    print "0"
    print
    print