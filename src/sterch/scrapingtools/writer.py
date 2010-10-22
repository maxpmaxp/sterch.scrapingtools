### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2008
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2008
#######################################################################

""" Scrapper for http://www.goldbergcoins.com/pastauction/index.shtml
    
$Id: writer.py 14192 2010-04-17 08:44:49Z maxp $
"""
__author__  = "Maxim Polscha (maxp@sterch.net)"
__license__ = "<undefined>" # необходимо согласование
__version__ = "$Revision: 14192 $"
__date__ = "$Date: 2010-04-17 11:44:49 +0300 (Сб, 17 апр 2010) $"

import csv
from string import strip
from threading import RLock

class CSVWriter:
    def __init__(self, filename):
        self.fields = []
        self.filename = filename
        self.lock = RLock()
        
    def writerow(self, d):
        self.lock.acquire()
        new_fields = [k for k in d.keys() if k not in self.fields ]
        self.fields += new_fields
        # dump fields
        f = open("%s.fields" % self.filename , "w")
        writer = csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_ALL)
        writer.writerow(self.fields)
        f.close()
        # dump object
        row = [d.get(k,'') for k in self.fields]
        f = open(self.filename , "a")
        writer = csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_ALL)
        writer.writerow(row)
        f.close()
        self.lock.release()
        
class SimpleCSVWriter:
    def __init__(self, filename, fields=None):
        self.filename = filename
        self.lock = RLock()
        self.isFirstRow = True
        self.fields = fields
        
    def writerow(self, d):
        self.lock.acquire()
        fields = self.fields if self.fields is not None else d.keys()
        if self.isFirstRow:
            # dump fields
            f = open(self.filename , "w")
            writer = csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_ALL)
            row = [k for k in fields]
            writer.writerow(row)
            f.close()
            self.isFirstRow = False
        # dump object
        row = [d.get(k,'') for k in fields]
        f = open(self.filename , "a")
        writer = csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_ALL)
        writer.writerow(row)
        f.close()
        self.lock.release()