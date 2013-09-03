### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012, 2013
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

US_STATE_CODES = \
{
    'ALABAMA' : 'AL',
    'ALASKA' : 'AK',
    'ARIZONA' : 'AZ',
    'ARKANSAS' : 'AR',
    'CALIFORNIA' : 'CA',
    'COLORADO' : 'CO',
    'CONNECTICUT' : 'CT',
    'DELAWARE' : 'DE',
    'DISTRICT OF COLUMBIA' : 'DC',
    'FLORIDA' : 'FL',
    'GEORGIA' : 'GA',
    'HAWAII' : 'HI',
    'IDAHO' : 'ID',
    'ILLINOIS' : 'IL',
    'INDIANA' : 'IN',
    'IOWA' : 'IA',
    'KANSAS' : 'KS',
    'KENTUCKY' : 'KY',
    'LOUISIANA' : 'LA',
    'MAINE' : 'ME',
    'MARYLAND' : 'MD',
    'MASSACHUSETTS' : 'MA',
    'MICHIGAN' : 'MI',
    'MINNESOTA' : 'MN',
    'MISSISSIPPI' : 'MS',
    'MISSOURI' : 'MO',
    'MONTANA' : 'MT',
    'NEBRASKA' : 'NE',
    'NEVADA' : 'NV',
    'NEW HAMPSHIRE' : 'NH',
    'NEW JERSEY' : 'NJ',
    'NEW MEXICO' : 'NM',
    'NEW YORK' : 'NY',
    'NORTH CAROLINA' : 'NC',
    'NORTH DAKOTA' : 'ND',
    'OHIO' : 'OH',
    'OKLAHOMA' : 'OK',
    'OREGON' : 'OR',
    'PENNSYLVANIA' : 'PA',
    'RHODE ISLAND' : 'RI',
    'SOUTH CAROLINA' : 'SC',
    'SOUTH DAKOTA' : 'SD',
    'TENNESSEE' : 'TN',
    'TEXAS' : 'TX',
    'UTAH' : 'UT',
    'VERMONT' : 'VT',
    'VIRGINIA' : 'VA',
    'WASHINGTON' : 'WA',
    'WEST VIRGINIA' : 'WV',
    'WISCONSIN' : 'WI',
    'WYOMING' : 'WY',
}

CA_PROVINCE_CODES = {
    'ALBERTA' : 'AB',            
    'BRITISH COLUMBIA' : 'BC',            
    'MANITOBA' : 'MB',            
    'NEW BRUNSWICK' : 'NB',
    'BRUNSWICK' : 'NB',            
    'NEWFOUNDLAND AND LABRADOR' : 'NL',
    'NEWFOUNDLAND' : 'NL',
    'LABRADOR' : 'NL',            
    'NORTHWEST TERRITORIES' : 'NT',            
    'NOVA SCOTIA' : 'NS',            
    'NUNAVUT' : 'NU',            
    'ONTARIO': 'ON',            
    'PRINCE EDWARD ISLAND' : 'PE',
    'PRINCE EDWARD' : 'PE',            
    'QUEBEC' : 'QC',            
    'SASKATCHEWAN' : 'SK',            
    'YUKON' : 'YT',                     
}

def is_fullname_suffix(s):
    """ Returns Trus if S is a full name suffix """
    return s.upper().strip() in ['JUNIOR', 'SENIOR', 'JR', 'JR.', 'SR', 'SR.', 'DR', 'DR.', 'PHD', "PHD.", "SIR", "ESQ", "ESQ.", "I", "II", "III", "IV", "V", "VI", "1ST", "2ND", "3RD", "4TH", "5TH", "6TH"]

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
    if not s: return ""
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
        title = suffix = ""
        # assume suffix comes first (f.e. Dr.)
        if is_fullname_suffix(allnames[0]):
            job["suffix"], allnames = allnames[0], allnames[1:]
        if schema.endswith("s"):
            # suffix comes last
            suffix = allnames[-1].upper().strip()
            if suffix and is_fullname_suffix(suffix):
                job["suffix"] = " ".join((job["suffix"], suffix)).strip()
                allnames = allnames[:-1]
        if schema[1] == "s":   
            # suffix comes 2nd
            if len(allnames) > 1:
                suffix = allnames[1]
                if suffix and is_fullname_suffix(suffix):
                    job["suffix"] = " ".join((job["suffix"], suffix)).strip()
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
        parsed = parser(allnames)
        suffix = parsed.pop("suffix", "")
        job.update(parsed,
                   suffix=" ".join((job["suffix"], suffix)).strip())
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
        while job[f] and job[f][-1] in (',',';','.',' '):
            job[f] = job[f][:-1]
    # work around mixed middlename & firstname when len(firstname)=1
    if len(job["middlename"]) > 1 and len(job["firstname"]) == 1:
        job["firstname"], job["middlename"] = job["middlename"], job["firstname"]
    # Work around suffix in the lastname
    if ' ' in job["lastname"]:
        pieces = job["lastname"].split(" ")
        for sfx, ln in ((pieces[0], " ".join(pieces[1:])),  
                        (pieces[-1], " ".join(pieces[:-1]))):
            if is_fullname_suffix(sfx):
                job["lastname"] = ln
                job["suffix"] = " ".join((job["suffix"], sfx)).strip()
                break
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
        while info[f] and info[f][-1] in (',',';','.',' '):
            info[f] = info[f][:-1]
    return info

def remove_aka(fullname):
    """ Removes AKA from the fullname given """
    fu = fullname.upper()
    for aka in ("AKA ", " AKA", "A.K.A.", "A.K.A", "A/K/A", "(ALSO KNOWN AS)", "ALSO KNOWN AS", " A K A ", 'A. K. A.',
                "FKA ", " FKA", "F.K.A.", "F.K.A", "F/K/A", "(FORMERLY KNOWN AS)", "FORMERLY KNOWN AS", " F K A ", 'F. K. A.',
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
                                    "REGIONAL", "SYSTEM", "HEALTH", "RURAL", "HIGHWAY", "DISTR", "PARTNERS", "BUILDING", "APTS", "COURTROOM",
                                    "CASINO", "COMMISSION", " CLUB ", "L.L.C.", "L.L.E.", "L.L.P.", "L.T.D." ] + US_STATE_CODES.keys() + CA_PROVINCE_CODES.keys())) or \
                any(map(lambda e:fullname.upper().strip().startswith(e), 
                            ['COURT ', 'BANK ', 'TRUST ', 'CTY ', 'TREAS ', "TAX ", "DEPT ", "DEPT. ", "B M V ", "CLUB ", ])))

def parse_city_state_zip(city_state_zip):
    """ Parses city_state_zip into a dict """
    city_state_zip = city_state_zip.replace(",", ", ").replace(".", ". ").strip()
    info = dict(city="", state="", zip="")
    try:
        info["city"], info["state"], info["zip"] = city_state_zip.rsplit(" ", 2)
    except:
        all_states = set(US_STATE_CODES.keys() + US_STATE_CODES.values() + CA_PROVINCE_CODES.keys() + CA_PROVINCE_CODES.values())
        try:
            p1, p2 = map(strip, city_state_zip.rsplit(" ", 1))
            # check if p1 is US zip :
            if all(map(lambda x:x in "0123456789-", p2)):
                info["zip"] = p2
                if p1.upper() in all_states:
                    info['state'] = p1
                else:
                    info['city'] = p1
            else:
                if p2.upper() in all_states:
                    info['city'], info['state'] = p1, p2
                else:
                    info['city'] = "%s %s" (p1, p2)     
        except:
            if city_state_zip.upper() in all_states:
                info['state'] = city_state_zip
            else:
                info['city'] = city_state_zip
                
    for f in ('city', 'state', 'zip'):
        info[f] = info[f].replace(u'\xa0','').strip()
        if info[f].endswith(",") : info[f] = info[f][:-1]
    info['state'] = info['state'].upper()
    return info

addr_headers = [ "PO BOX", "P.O. BOX","P O BOX", "POBOX", 'PO ', "P O", "P.O.", "P. O.", 
                'RURAL ROUTE', 'RR ', "R R", "R.R.", "R. R.",
                'HIGHWAY CONTRACT', 'HC ', "H C", "H.C.", "H. C.",
                ] + map("".join,product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', string.digits, string.digits)) + ['0','1','2','3','4','5','6','7','8','9',]

def normalize_address(address):
    """ An address must start with an integer, 
        the letter P, (PO BOX, P.O. BOX, etc), RR, the word Rural (as in Rural Route), 
        HC, the word Highway (as in Highway Contract 77…), 
        or a letter followed immediate by at least two integers, i.e. (like this W7905 State Road 29, or N4116 Springbrook Rd) """
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

def is_normal_address(address):
    """ Returns True is address is a normal one, See normalize_address for more """
    if not address: return False
    address = address.upper()
    return any(map(lambda _: address.startswith(_), addr_headers))

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
    if not page: return
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

def smart_fullname_cmp(fullname_variant, **person):
    """ Compares fullname against person's lastname, firstname, middlename and suffix """
    fullname_factories = ( lambda **d: " ".join(map(lambda _f: d.get(_f) or '', ('lastname', 'firstname', 'middlename', 'suffix'))),
                       lambda **d: " ".join(map(lambda _f: d.get(_f) or '', ('lastname', 'firstname', 'middlename'))),
                       lambda **d: " ".join(map(lambda _f: d.get(_f) or '', ('lastname', 'firstname'))) + (" %s" % d['middlename'][0] if d.get('middlename') else ''),
                       lambda **d: " ".join(map(lambda _f: d.get(_f) or '', ('lastname', 'firstname'))),
                      )
    return any(map(lambda fn_factory: smart_cmp(fn_factory(**person), fullname_variant), fullname_factories))

def smart_match_fullname(text, **person):
    """ Returns True if person's name is in the text provided """
    text = text.upper()
    for _ in '.,()"\':0123456789!@#$^%&*_~`</>\\': text = text.replace(_," ")
    tokens = filter(None, text.split()) 
    for j in xrange(0, len(tokens) - 2):
        pieces = tokens[j:]
        for i in (2,3):
            _name = " ".join(pieces[:i])
            if smart_fullname_cmp(_name, **person):
                return True
    return False