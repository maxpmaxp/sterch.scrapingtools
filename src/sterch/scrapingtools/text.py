### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012
#######################################################################

"""Text processing functions
"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

import csv
import os.path
import re

__MY__PATH__ = os.path.dirname(os.path.abspath(__file__))
glEntities = dict([p for p in csv.reader(open(os.path.join(__MY__PATH__,"entities.csv"),"rU")) ]) 

def striptags(text):
    """ strips tags from the text"""
    return re.sub("<[^>]+>", " ", text)

def replace_html_entities(text):
    """ replaces HTML entities from the text """
    global glEntities
    # replace numeric entities
    _numentities = set(re.findall("(&#\d+;)", text))
    for entity in _numentities:
        code = entity[2:-1]
        text = text.replace(entity, unichr(int(code)))
    # replace character entities
    _entities = set(re.findall("(&[a-zA-Z0-9]+;)", text))
    for entity in _entities:
        literal = entity[1:-1] 
        if literal in glEntities:
            try:
                text = text.replace(entity, unichr(int("0x%s" % glEntities[literal], 16)))
            except Exception:
                pass 
    return text

def normalize(s):
    ss = s
    _javascript = re.findall("(<script.*?>.*?</script>)", ss, re.MULTILINE|re.DOTALL)
    for script in _javascript:
        ss = ss.replace(script,' ')
    _styles = re.findall("(<style.*?>.*?</style>)", ss, re.MULTILINE|re.DOTALL)
    for style in _styles:
        ss = ss.replace(style,' ')
    ss =  replace_html_entities(striptags(ss))
    ss = ss.replace("\r",' ')
    ss = ss.replace("\n",' ')
    ss = ss.replace("\t",' ')
    ss = ss.strip()
    while '  ' in ss: ss=ss.replace('  ', ' ')
    return ss

def tofilename(name):
    n = name
    illegal=":,|<>\\/\"'~`!@#$%^&*()\n\r\t?;"
    for s in illegal : n = n.replace(s,'')
    return n

def parse_fullname(fullname):
    """ Parses a fullname into pieces: firstname, lastname, middlename, suffix.
        Returns dict """
    job = dict()
    job['firstname'] = job['lastname'] = job['middlename'] = job['suffix'] = ''
    if ", " in fullname:
        _allnames = fullname.split(", ",1)
        allnames = [_allnames[0],] + _allnames[1].split()
    else:
        allnames = filter(None, fullname.split())
    job["suffix"] = ''
    if allnames:
        if allnames[0].upper() in ('STATE', 'CITY', 'TOWNSHIP', 'GOVERNMENT') or \
           allnames[-1].upper() in ('INC', 'INC.', 'LLC.', 'LLC', 'COMPANY', 'LTD', 'LTD.', 'CO', 'CORP', 'CORP.', 'NA', 'N.A.', 'COOPERATIVE') or \
           'BANK' in allnames or 'UNIVERSITY' in allnames or 'UNION' in allnames:
            job["lastname"] = fullname
            return job
           
        suffix = allnames[-1].upper().strip()
        if suffix in ['JR', 'JR.', 'SR', 'SR.', "I", "II", "III", "IV", "1ST", "2ND", "3RD", "4TH", "5TH"]:
            job["suffix"] = suffix
            allnames = allnames[:-1]
    if len(allnames) == 1:
        job['lastname'] = allnames[0]
    elif len(allnames) == 2:
         job['lastname'] = allnames[0]
         job['firstname'] = allnames[1]
    elif len(allnames) > 2:
         job['lastname'] = allnames[0]
         job['firstname'] = allnames[1]
         job['middlename'] = " ".join(allnames[2:])
    # postprocess middlename
    if "; " in job['middlename']:
        job['middlename'], job['suffix'] = job['middlename'].split("; ",1)
    for f in ('firstname', 'middlename', 'lastname', 'suffix'):
        for c in (',','.',';'):
            job[f] = job[f].replace(c," ")
        while "  " in job[f]: job[f] = job[f].replace("  "," ")
    return job

def parse_fulladdress(fulladdress):
    """ Parses fulladdress into pieces: US format. 
        Returns dict containing address, zip, state, city """
    
    fulladdress = fulladdress.strip()
    info = dict(address="", zip="", state="", city="")
    if " " not in fulladdress:
        info["address"] = fulladdress
        return info
    rest, info["zip"] = fulladdress.rsplit(" ", 1)
    if len(info["zip"]) == 2: 
        info['state'] = info['zip']
        info['zip'] = ''
    if ", " not in  rest:
        info["address"] = rest
        return info
    rest, info["state"] = rest.rsplit(", ", 1)
    if ", " not in  rest:
        info["address"] = rest
        return info
    info["address"], info["city"] = rest.rsplit(", ", 1)
    for k, v in info.items():
        info[k] = v.strip()
    for f in ('address', 'state', 'city', 'zip'):
        if info[f] and info[f][-1] in (',',';','.'):
            info[f] = info[f][:-1]
    return info