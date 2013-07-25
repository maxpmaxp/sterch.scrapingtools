### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2013
#######################################################################

"""Text processing functions (for courts data scraping)
"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

import re
from text import is_person, smart_cmp, normalize
from threading import Lock

def is_plaintiff(descr):
    """ If a string description is a plaintiff description """
    return not is_attorney(descr) and any(map(lambda s: s in descr.upper(), ('PLAINTIFF', 'PLTF', 'PETITIONER', 'CLAIMANT', 'COMPLAINANT', 'PROTECTED', 'APPELLANT', 'LIENEE')))
    
def is_defendant(descr):
    """ If a string description is a defendant description """
    return not is_attorney(descr) and any(map(lambda s: s in descr.upper(), ('DEFENDANT', 'DEFT', 'RESPONDENT', 'RESPONDER', 'RESTRAINED', 'APPELLEE', 'LIENOR')))

def is_attorney(descr):
    """ If a string description is a attorney description """
    return any(map(lambda s: s in descr.upper(), ('ATTORNEY','ATTNY')))

def is_valid_attorney(attorney, defendant_fullname=None):
    """ Returns False if attorney is empty or is defendant """
    if not attorney: return False
    if defendant_fullname:
        if smart_cmp(defendant_fullname, attorney): return False
    attorney = normalize(attorney).upper().strip()
    if any(map(lambda s: s in attorney, ['NO ATTORNEY', 'PRO SE', 'UNKNOWN' , 'PRO PRE', "PROSE", "PROPRE", "PROPER", "PRO PER", 'UNREPRESENTED',
                                         'N/A', 'NO-ATTORNEY', 'NO ATTORNEY', 'PRO SE', 'UNKNOWN', 'PUBLIC', 'DEFENDER', 'DEFENDANT', 'RESPONDENT','RESPONDER',])) \
        or any(map(lambda s: s==attorney, ['NO', 'NONE', 'NA', 'N.A.', 'UNK', 'UNKNWN',])):
           return False
    return True

def extract_description(page, default=None):
    """ Extracts civil case description. Usually it is used for a docket """
    _page = page.upper()
    desc = None
    for _m in ('PERSONAL INJURY/PROPERTY DAMAGE - NON-VEHICLE', 'PERSONAL INJURY/PROPERTY DAMAGE', 'PROPERTY DAMAGE - NON-VEHICLE',
               'PERSONAL INJURY - NON-VEHICLE', 'PERSONAL INJURY', 'PROPERTY DAMAGE',
               'FORECLOSURE', 'MORTGAGE', 'DAMAGES', 'MONEY DEBT', "CIVIL MONEY ONLY 1 DEF", "CIVIL MONEY ONLY", "CONTRACTS/ACCOUNTS/MONEY OWED", "MONEY COMPLAIN", 
              "ALL OTHER CIVIL 1 DEF", "ALL OTHER CIVIL 2 DEF", "ALL OTHER CIVIL 3 DEF", "ALL OTHER CIVIL", "OTHER CIVIL", "MONEY CIVIL", "MONEY DUE",
              "APPEAL WORKERS COMPENSATION (A)", "APPEAL WORKERS COMPENSATION (B)", "APPEAL WORKERS COMPENSATION (C)", "APPEAL WORKERS COMPENSATION (D)",
              "APPEAL WORKERS COMPENSATION", "WORKERS COMPENSATION",
              "OTHER TORT PERSONAL INJURY (A)", "OTHER TORT PERSONAL INJURY (B)", "OTHER TORT PERSONAL INJURY (C)", "OTHER TORT PERSONAL INJURY (D)",
              "OTHER TORT PERSONAL INJURY", "TORT PERSONAL INJURY", "PERSONAL INJURY",
              "BMV FORM 2255 ADM LIC SUSP (ALS)", "BMV FORM 2255 ADM LIC SUSP", "SMALL CLAIM"):
        if _m in page:
            desc = _m
            break
    return desc or default
        
def extract_date(text):
    """ Extracts a date from the text. Returns None is no suitable date was found """
    if text is None: return None
    all_formats = ("\d{1,2}/\d{1,2}/\d\d\d\d",
                   "\d{1,2}-\d{1,2}-\d\d\d\d",
                   "\d{1,2}/\w\w\w/\d\d\d\d",
                   "\d{1,2}-\w\w\w-\d\d\d\d",
                   "\w\w\w \d{1,2} \d\d\d\d",
                   "\d{1,2} \w\w\w \d\d\d\d",
                   "\d{1,2}/\d{1,2}/\d\d",
                   "\d{1,2}-\d{1,2}-\d\d",
                   "\d{1,2}/\w\w\w/\d\d",
                   "\d{1,2}-\w\w\w-\d\d",
                   "\w\w\w \d{1,2} \d\d",
                   "\d{1,2} \w\w\w \d\d",
                  )
    for fmt in all_formats:
        lst = re.findall(fmt, text)
        if lst: 
            return lst[0]

def extract_money(text):
    """ Extracts money amount from the text given """
    if text is None: return None
    fmt = "\$\s?(?:\d+,\d\d\d)?\d*(?:\.\d{1,2})?"
    lst = re.findall(fmt, text)
    amount = None
    if lst: 
        try:
            amount = float(lst[0].replace("$","").replace(",","").strip())
        except ValueError:
            pass
    return amount 

def is_john_doe(**case):
    """ True if a case is about John Doe as defendant """
    fullname = case.get('fullname')
    if not fullname:
        fullname = " ".join(filter(None, [case[f] if case.get(f,'') else '' for f in ('lastname', 'firstname', 'middlename', 'suffix')]))
    fullname = "".join([ c for c in fullname.upper() if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ "])    
    fullname = fullname.strip()
    if not fullname: return True
    _lastname = "".join([ c for c in case.get('lastname','').upper() if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"])
    _firstname = "".join([ c for c in case.get('firstname','').upper() if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"])
    pieces = filter(None, fullname.split())
    return is_person(fullname) and \
            (any(map(lambda s: s in fullname, ['UNKSP', 'UNK SP', 'UNK SPOUSE', 'DOE JOHN', 'DOE JANE', 'JOHN DOE', 'JANE DOE', 'UNKNOWN', ' DOES ', ' DOE '])) or
             any(map(lambda s: s in pieces, ("DOE", "DOES", "UNKNOWN", "UNK", "SPOSE", "TENANT",))))
            
class SequenceState(object):
    """ Sequence pulling state """
    
    def __init__(self, lastnumber, limit):
        self.lock = Lock()
        self._lastnumber = lastnumber
        self.missing = set()
        self.limit = limit
        
    def get_lastnumber(self):
        with self.lock:
            return self._lastnumber
        
    def set_lastnumber(self, v):
        with self.lock:
            if v > self._lastnumber:
                self._lastnumber = v
                
    lastnumber = property(get_lastnumber, set_lastnumber)
    
    def add_to_missing(self, v):
        with self.lock:
            self.missing.add(v)
            
    def is_finished(self):
        with self.lock:
            return set(xrange(self._lastnumber + 1, self._lastnumber + self.limit)).issubset(self.missing)