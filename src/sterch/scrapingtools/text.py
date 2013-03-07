### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012,2013
#######################################################################

"""Text processing functions
"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

import csv
import os.path
import re, string
import fullname as modfullname

from itertools import product
from string import strip

__MY__PATH__ = os.path.dirname(os.path.abspath(__file__))
glEntities = dict([p for p in csv.reader(open(os.path.join(__MY__PATH__,"entities.csv"),"rU")) ]) 

def is_fullname_suffix(s):
    """ Returns Trus if S is a full name suffix """
    return s.upper().strip() in ['JUNIOR', 'SENIOR', 'JR', 'JR.', 'SR', 'SR.', "I", "II", "III", "IV", "V", "VI", "1ST", "2ND", "3RD", "4TH", "5TH", "6TH"]

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
    ss = ss.replace(u"\xa0",' ')
    ss = ss.strip()
    while '  ' in ss: ss=ss.replace('  ', ' ')
    return ss

def tofilename(name):
    n = name
    illegal=":,|<>\\/\"'~`!@#$%^&*()\n\r\t?;"
    for s in illegal : n = n.replace(s,'')
    return n

def parse_fullname(fullname, schema="lfms"):
    """ Parse fullname using a schema.
        l - lastname
        m - firstname
        f - firstname
        s - suffix
        into pieces: firstname, lastname, middlename, suffix.
        Returns dict     """
    job = dict()
    job['firstname'] = job['lastname'] = job['middlename'] = job['suffix'] = ''
    if not is_person(fullname):
        job["lastname"] = fullname
        return job
    if ", " in fullname:
        _allnames = fullname.split(", ",1)
        allnames = [_allnames[0],] + _allnames[1].replace(","," ").split()
    else:
        allnames = fullname.split()
    allnames = filter(None, allnames)
    job["suffix"] = ''
    if allnames:
        suffix = ""
        if schema.endswith("s"):
            # suffix comes last
            suffix = allnames[-1].upper().strip()
            if suffix and is_fullname_suffix(suffix):
                job["suffix"] = suffix
                allnames = allnames[:-1]
        if schema[1] == "s":   
            # suffix comes 2nd
            if len(allnames) > 1:
                suffix = allnames[1]
                if suffix and is_fullname_suffix(suffix):
                    job["suffix"] = suffix
                    allnames = [allnames[0],] + allnames[2:]
            
    if len(allnames) == 1:
        job['lastname'] = allnames[0]
    else:
        if schema in ("lfms", "lsfm"):
            parser = modfullname.parse_lfms
        elif schema in ("lmfs", "lsmf"):
            parser = modfullname.parse_lmfs
        elif schema == "fmls":
            parser = modfullname.parse_fmls
        elif schema == "flms":
            parser = modfullname.parse_flms
        else:
            raise ValueError("Unknown fullname schema %s" % schema)
        job.update(parser(allnames))
    # postprocess middlename
    if "; " in job['middlename']:
        job['middlename'], job['suffix'] = job['middlename'].split("; ",1)
    for f in ('firstname', 'middlename', 'lastname', 'suffix'):
        for c in (',','.',';','$'):
            job[f] = job[f].replace(c," ")
        while "  " in job[f]: job[f] = job[f].replace("  "," ")
    # I and V are suffixes only if there is a middlename
    if not job["middlename"] and job["suffix"].upper() in ('V', 'I'):
        job["middlename"] = job["suffix"]
        job["suffix"] = ""
    # strip spaces
    for f in ("firstname", "lastname", "middlename", "suffix"):
        job[f] = job[f].strip()
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

def remove_aka(fullname):
    """ Removes AKA from the fullname given """
    fu = fullname.upper()
    for aka in ("AKA ", " AKA", "A.K.A.", "A.K.A", "A/K/A", "(ALSO KNOWN AS)", "ALSO KNOWN AS", " A K A ", 'A. K. A.',
                "DBA ", " DBA", "D.B.A.", "D/B/A", "(DOING BUSINESS AS)", "DOING BUSINESS AS", " D B A ", 'D. B. A.', 
                'IN HER OFFICIAL CAPACITY', 'IN HIS OFFICIAL CAPACITY', 'IN HER CAPACITY', 'IN HIS CAPACITY'):
        if aka in fu:
            fu = fu.split(aka,1)[0]
    return fu.strip()

def is_person(fullname):
    """ Checks whether a name given is person's name """
    return not (any(map(lambda e:fullname.upper().strip().endswith(e), 
                            [' NA', 'LLC', ' INC', ' CO', ' CORP', 'LLP', 'LTD', 'LLC', 'INC.', ' CO.', ' CORP.', 'LLP.', 'LTD.' , ' LLE', ' LLE.', ' TRUST', ' COURT',
                             " ORG", " ORG.", " CTY", " TREAS", " TAX", " DEPT", " DEPT.", " B M V", " CLUB", ])) or \
               any(map(lambda e:e in fullname.upper(), ['ACADEM', 'HOSPITAL', 'COMPANY', 'CO.', 'SERVICES', 'AUTHORITY', 'ASSOC', 'N.A.', ' BANK', ' BANK.',  
                                    ' INC', 'LLC', ' CORP', 'LLP', 'LLC', 'LTD', 'STATE', 'CITY', 'COUNTY', ' TRUST ', ' COURT ', 'DPT', 'DPT.'
                                    'TOWNSHIP', 'GOVERNMENT', 'UNIVERSITY', "UNION", " BANK ", "COOPERATIVE", "ENTERPR", "DISTRICT",  "COMPANY", "PARTNERSHIP",
                                    "COMMONWEALTH", "CONDOMINIUM", "VILLAGE", "SHOP", "APARTMENTS", "&", "DBA", " AND ", "BUREAU", "TWP", "MARKET",
                                    "STUDIO", "ASSOC", ' TRUST ', 'NETWORK', 'LIMITED', 'DEPARTMENT', 'UNIT', 'CREDIT', 'TENANT', 'UNKNOWN', 'N/A', 'PRISON',
                                    "HOSPITAL", "OFFICE", "AGENCY", "ORGANISATION", "ORGANIZATION", "CLINIC", "CLINIQUE", "BANQUE", "SERVICE", 
                                    "CORPORATION", "CHURCH", "HOTEL", "SUITES", "NATIONAL", "SOCIETY", "BUSINESS", "CENTER", "SECURITY",
                                    "FINANCE", "EDUCATION", "MEDICAL", "OFFICER", "MANAGEMENT", "MGMT", "EQUIPMENT", "INSURANCE", "GROUP",
                                    "COLLEGE", "DEVELOPMENT", "RESTAURANT", "SCHOOL", "COURTHOUSE", " CTY ", " TREAS ", "TREASURER",
                                    "COMMISSION", "INDUSTRIAL", "HEIRS", "DIRECTOR", "ADMINISTRATOR", "HOUSING", "HOMESTEAD", "SURVIVING", 
                                    "ASSIGNS", "EXEC", "DEVISEE", " TAX ", " DEPT ", " OF ", "SUCCESSORS", "APPEAL", 
                                    "BMV", " B M V ", "B.M.V.", "B. M. V.", "B/M/W",
                                    "REGIONAL", "SYSTEM", "HEALTH", "RURAL", "HIGHWAY",
                                    "CASINO", "COMMISSION" , " CLUB ", ])) or \
                any(map(lambda e:fullname.upper().strip().startswith(e), 
                            ['COURT ', 'BANK ', 'TRUST ', 'CTY ', 'TREAS ', "TAX ", "DEPT ", "DEPT. ", "B M V ", "CLUB ", ])))

def parse_city_state_zip(city_state_zip):
    """ Parses city_state_zip into a dict """
    city_state_zip = city_state_zip.replace(",", ", ").replace(".", ". ")
    info = dict(city="", state="", zip="")
    try:
        info["city"], info["state"], info["zip"] = city_state_zip.rsplit(" ", 2)
    except:
        try:
            p1, p2 = city_state_zip.rsplit(" ", 1)
            # check if p1 is US zip :
            if all(map(lambda x:x in "0123456789-", p2)):
                info['state'], info['zip'] = p1, p2
            else:
                info['city'], info['state'] = p1, p2
        except:
            info['city'] = city_state_zip
    for f in ('city', 'state', 'zip'):
        info[f] = info[f].replace(u'\xa0','')
        if info[f].endswith(",") : info[f] = info[f][:-1]
    info['state'] = info['state'].upper()
    return info

def normalize_address(address):
    """ An address must start with an integer, 
        the letter P, (PO BOX, P.O. BOX, etc), RR, the word Rural (as in Rural Route), 
        HC, the word Highway (as in Highway Contract 77…), 
        or a letter followed immediate by at least two integers, i.e. (like this W7905 State Road 29, or N4116 Springbrook Rd) """
    l = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    addr_headers = [ "PO BOX", "P.O. BOX","P O BOX", "POBOX", 'PO ', "P O", "P.O.", "P. O.", 
                    'RURAL ROUTE', 'RR ', "R R", "R.R.", "R. R.",
                    'HIGHWAY CONTRACT', 'HC ', "H C", "H.C.", "H. C.",
                    ] + map("".join,product(l, string.digits, string.digits)) + ['0','1','2','3','4','5','6','7','8','9',]
    addr = address.strip().upper() 
    for suffix in addr_headers:
        if addr.startswith(suffix):
            return addr    
    min_match = None
    for suffix in addr_headers:
        if suffix in addr:
            min_match = min(min_match, addr.find(suffix)) if min_match is not None else addr.find(suffix)
    retval = address if min_match is None else addr[min_match:]
    return retval

def get_block(page, start, end):
    """ Returns a block as described by start and end markers.
        If start marker not in page - returns none
        If end marker is not in page - returns all after the start marker
    """
    if page is None: return None
    if start in page:
        return page.split(start,1)[1].split(end,1)[0]

def get_head(page, marker):
    """ Returns page content before the marker """
    if page is None: return None
    if marker in page:
        return page.split(marker,1)[0]
    
def get_tail(page, marker):
    """ Returns page content after the marker """
    if page is None: return None
    if marker in page:
        return page.split(marker,1)[1]

def parse_ff_mapping(page, ff_mapping, end_marker):
    """ Parses fields mapping """
    info = dict()
    for k,v in ff_mapping.iteritems():
        info[k] = normalize(page.split(v,1)[1].split(end_marker,1)[0]) if v in page else ''
    return info

def walk_table(page, row_marker="</tr>", cell_marker="</td>", min_cols_number=None, do_normalize=False, use_start_markers=False):
    """ Generates table rows splitted by row and cell markers as lists.
        if normalize  ---- normalizes the result,
        if min_cols_number is not None - filters all rows with a number of columns less then the one.
        Normally row_marker and cell_marker mark the end on the block except when use_start_markers is set to True
    """
    row_slices = page.split(row_marker)[:-1] if not use_start_markers else page.split(row_marker)[:-1]
    for row in row_slices:
        cols = row.split(cell_marker)[:-1] if not use_start_markers else row.split(cell_marker)[:-1]
        if min_cols_number and len(cols) < min_cols_number: continue
        if do_normalize: cols = map(normalize, cols)
        yield cols
        
def smart_cmp(s1, s2):
    """ Compares 2 strings as sets of words"""
    _s1, _s2 = map(lambda s:s.upper().replace(".", " ").replace(",", " ").strip(),  (s1, s2))
    _s1, _s2 = map(lambda s: sorted(filter(None, s.split())), (_s1, _s2))
    _s1, _s2 = map(lambda s: map(strip, s), (_s1, _s2))
    return _s1 == _s2