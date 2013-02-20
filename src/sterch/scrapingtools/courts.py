### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2013
#######################################################################

"""Text processing functions (for courts data scraping)
"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

import re
from text import is_person, smart_cmp

def is_plaintiff(descr):
    """ If a string description is a plaintiff description """
    return not is_attorney(descr) and any(map(lambda s: s in descr.upper(), ('PLAINTIFF', 'PETITIONER', 'CLAIMANT', 'COMPLAINANT', 'PROTECTED')))
    
def is_defendant(descr):
    """ If a string description is a defendant description """
    return not is_attorney(descr) and any(map(lambda s: s in descr.upper(), ('DEFENDANT','RESPONDENT','RESPONDER','RESTRAINED')))

def is_attorney(descr):
    """ If a string description is a attorney description """
    return any(map(lambda s: s in descr.upper(), ('ATTORNEY','ATTNY')))

def is_valid_attorney(attorney, defendant_fullname=None):
    """ Returns False if attorney is empty or is defendant """
    if not attorney: return False
    if defendant_fullname:
        if smart_cmp(defendant_fullname, attorney): return False
    attorney = attorney.upper()
    if any(map(lambda s: s in attorney, ['NO ATTORNEY', 'PRO SE', 'UNKNOWN' , 'PRO PRE', "PROSE", "PROPRE", "PROPER", "PRO PER"])):
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
              "BMV FORM 2255 ADM LIC SUSP (ALS)", "BMV FORM 2255 ADM LIC SUSP"):
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
                   "\d{1,2}/\d{1,2}/\d\d",
                   "\d{1,2}-\d{1,2}-\d\d",
                   "\d{1,2}/\w\w\w/\d\d",
                   "\d{1,2}-\w\w\w-\d\d",
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
    fullname = fullname.upper()    
    
    _lastname = case.get('lastname','').upper()
    _firstname = "".join([ c for c in case.get('firstname','').upper() if c in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"])
    
    return is_person(fullname) and \
            (any(map(lambda s: s in fullname, ['UNKSP', 'UNK SP', 'UNK SPOUSE', 'DOE JOHN', 'DOE JANE', 'JOHN DOE', 'JANE DOE', 'UNKNOWN'])) \
             or ((_lastname == "DOE" or _lastname == "DOES" or _lastname.startswith("DOE ") or _lastname.startswith("DOES ")) and _firstname in ('JOHN', 'JANE', ''))
            )