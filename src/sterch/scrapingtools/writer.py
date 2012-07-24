### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012
#######################################################################

""" CSV writers
"""
__author__  = "Maxim Polscha (maxp@sterch.net)"
__license__ = "ZPL"

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