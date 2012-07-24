### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012
#######################################################################

"""Output functions
"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

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