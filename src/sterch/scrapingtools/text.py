### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012-2017
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
    fullname = fullname.replace(","," ")
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
    for aka in (" AKA ", "A.K.A.", "A.K.A", "A/K/A", "(ALSO KNOWN AS)", "ALSO KNOWN AS", " A K A ", 'A. K. A.',
                " FKA ", "F.K.A.", "F.K.A", "F/K/A", "(FORMERLY KNOWN AS)", "FORMERLY KNOWN AS", " F K A ", 'F. K. A.',
                " DBA ", "D.B.A.", "D/B/A", "(DOING BUSINESS AS)", "DOING BUSINESS AS", " D B A ", 'D. B. A.',
                'IN HER OFFICIAL CAPACITY', 'IN HIS OFFICIAL CAPACITY', 'IN HER CAPACITY', 'IN HIS CAPACITY',
                'DESCRIBED AS', "NOW KNOWN AS"):
        if aka in fu:
            fu = fu.split(aka,1)[0]
    return fu.strip()

def is_person(fullname):
    """ Checks whether a name given is person's name """
    return not (any(map(lambda e:fullname.upper().strip().endswith(e), 
                            [' NA', 'LLC', ' INC', ' CO', ' CORP', 'LLP', 'LTD', 'LLC', 'INC.', ' CO.', ' CORP.', 'LLP.', 'LTD.' , ' LLE', ' LLE.', ' TRUST', ' COURT',
                             " ORG", " ORG.", " CTY", " TREAS", " TAX", " DEPT", " DEPT.", " B M V", " CLUB", " P.C.", " PC", ])) or \
               any(map(lambda e:e in fullname.upper(), ['ACADEM', 'HOSPITAL', 'COMPANY', 'CO.', 'SERVICES', 'AUTHORITY', 'ASSOC', 'N.A.', ' BANK', ' BANK.',  
                                    ' INC', 'LLC', ' CORP', 'LLP', 'LLC', 'LTD', 'PLC', 'STATE', 'CITY', 'COUNTY', ' TRUST ', ' COURT ', 'DPT', 'DPT.'
                                    'TOWNSHIP', 'GOVERNMENT', 'UNIVERSITY', "UNION", " BANK ", "COOPERATIVE", "ENTERPR", "DISTRICT",  "COMPANY", "PARTNERSHIP",
                                    "COMMONWEALTH", "CONDOMINIUM", "VILLAGE", "SHOP", "APARTMENTS", "&", " DBA", " AND ", "BUREAU", "TWP", "MARKET",
                                    "STUDIO", "ASSOC", ' TRUST ', 'NETWORK', 'LIMITED', 'DEPARTMENT', 'UNIT', 'CREDIT', 'TENANT', 'UNKNOWN', 'N/A', 'PRISON',
                                    "HOSPITAL", "OFFICE", "AGENCY", "ORGANISATION", "ORGANIZATION", "CLINIC", "CLINIQUE", "BANQUE", "SERVICE", 
                                    "CORPORATION", "CHURCH", "HOTEL", "SUITES", "NATIONAL", "SOCIETY", "BUSINESS", "CENTER", "SECURITY",
                                    "FINANCE", "EDUCATION", "MEDICAL", "OFFICER", "MANAGEMENT", "MGMT", "EQUIPMENT", "INSURANCE", "GROUP",
                                    "COLLEGE", "DEVELOPMENT", "RESTAURANT", "SCHOOL", "COURTHOUSE", " CTY ", " TREAS ", "TREASURER",
                                    "COMMISSION", "INDUSTRIAL", "HEIRS", "DIRECTOR", "ADMINISTRATOR", "HOUSING", "HOMESTEAD", "SURVIVING", 
                                    "ASSIGNS", "EXEC", "DEVISEE", " TAX ", " DEPT ", " OF ", "SUCCESSORS", "APPEAL", 
                                    "BMV", " B M V ", "B.M.V.", "B. M. V.", "B/M/W",
                                    "REGIONAL", "SYSTEM", "HEALTH", "RURAL", "HIGHWAY", "DISTR", "PARTNERS", "BUILDING", "APTS", "COURTROOM",
                                    "CASINO", "COMMISSION", " CLUB ", "L.L.C.", "L.L.E.", "L.L.P.", "L.T.D.", " P.C. ", " PC ",
                                    "CURRENCY", "COMPENSAT", "ALL OTHERS", "CONTRACTOR", "INDEMNITY", "AMERICAN", "WIRELESS", "PACIFIC",
                                    "SPECIALIST", "SURGERY", "WHOLESALE", "CONCRETE", "ENERGY", "MUTUAL", "SUPPLY"])) or \
                any(map(lambda e:fullname.upper().strip().startswith(e), 
                            ['COURT ', 'BANK ', 'TRUST ', 'CTY ', 'TREAS ', "TAX ", "DEPT ", "DEPT. ", "B M V ", "CLUB ", "DBA"])) or \
                any(map(lambda e:fullname.upper().strip() == e, 
                            US_STATE_CODES.keys() + CA_PROVINCE_CODES.keys())))

RE_US_ZIP = re.compile(r'^\d{5}(?:[-\s]\d{4})?$')
RE_CA_ZIP = re.compile(r'^[ABCEGHJKLMNPRSTVXY]\d[ABCEGHJ-NPRSTV-Z][ ]?\d[ABCEGHJ-NPRSTV-Z]\d$', re.IGNORECASE)

ALL_STATES_TOKENS = set(US_STATE_CODES.keys() + US_STATE_CODES.values()
                        + CA_PROVINCE_CODES.keys() + CA_PROVINCE_CODES.values())


def parse_city_state_zip(city_state_zip):
    """ Parses city_state_zip into a dict """
    city_state_zip = normalize(city_state_zip.replace(",", ", ").replace(".", ". ").strip())
    if city_state_zip:
        # normalize commas
        _m = " ,"
        while _m in city_state_zip:
            city_state_zip = city_state_zip.replace(_m, ",")
    info = dict(city="", state="", zip="")

    pieces = city_state_zip.split(" ")
    # Get zip, if exists
    if RE_US_ZIP.match(pieces[-1]) or RE_CA_ZIP.match(pieces[-1]):
        info["zip"] = pieces.pop()
    elif len(pieces) >= 2:
        ca_zip_candidate = pieces[-2] + " " + pieces[-1]
        if RE_CA_ZIP.match(ca_zip_candidate):
            info["zip"] = " ".join(pieces[-2:])
            pieces = pieces[:-2]

    # parse state of 3,2,1 tokens
    for tlen in (3, 2, 1):
        if len(pieces) >= tlen:
            token = " ".join(pieces[-tlen:]).upper()
            if token in ALL_STATES_TOKENS:
                info["state"] = token
                pieces = pieces[:-tlen]

    # the rest is city
    info["city"] = " ".join(pieces)
                
    for f in ('city', 'state', 'zip'):
        info[f] = info[f].replace(u'\xa0', '').strip()
        if info[f].endswith(","):
            info[f] = info[f][:-1]

    return info

addr_headers = [ "PO BOX", "P.O. BOX","P O BOX", "POBOX", 'PO ', "P O", "P.O.", "P. O.", 
                'RURAL ROUTE', 'RR ', "R R", "R.R.", "R. R.",
                'HIGHWAY CONTRACT', 'HC ', "H C", "H.C.", "H. C.",
                ] + map("".join,product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', string.digits, string.digits)) + ['0','1','2','3','4','5','6','7','8','9',]

known_addr_prefixes = [ "APT", "APARTMENT", "FLOOR", "SUITE", "STE", "UNIT", "UNT", "FLR", "MAIL STOP", "STOP", ]

def _find_addr_header_position(address):
    addr = address.strip().upper() 
    for suffix in addr_headers:
        if addr.startswith(suffix):
            return 0    
    min_match = None
    for suffix in addr_headers:
        if suffix in addr:
            min_match = min(min_match, addr.find(suffix)) if min_match is not None else addr.find(suffix)
    if min_match is None:
        raise IndexError("No known address header found")
    return min_match
    
def normalize_address(address):
    """ WARNING: OBSOLETE, just for backward compatibility.
        Use parse_and_normalize_streetaddress instead.
        An address must start with an integer, 
        the letter P, (PO BOX, P.O. BOX, etc), RR, the word Rural (as in Rural Route), 
        HC, the word Highway (as in Highway Contract 77…), 
        or a letter followed immediate by at least two integers, i.e. (like this W7905 State Road 29, or N4116 Springbrook Rd) """
    addr = address.strip().upper()
    try:
        addr = addr[_find_addr_header_position(addr):]
    except IndexError:
        pass
    return addr

def parse_and_normalize_streetaddress(address):
    """ Returns dict:
        address - normalized street address
        company - company name if given
        prefix - unparsed prefix
    """
    # determine if known prefix comes before address
    info = dict(address="", company="", prefix="")
    if not address: return info
    addr = address.strip().upper() 
    try:
        header_pos = _find_addr_header_position(addr)
    except IndexError:
        # Unknown address format, remains unchanged
        info["address"] = addr
        return info
    if any(map(lambda _: _ == addr, known_addr_prefixes)):
        # Nothing to parse one of known prefixes (which is just a corner-case)
        info["address"] = addr
        return info
    elif header_pos == 0:
        if addr[0] in string.digits:
            # work around addresses like: 1st Floor 1230 main Str.
            for pattern in [ r"#?\d+\w{0,2}\s+" + _ for _ in known_addr_prefixes ]:
                if re.match(pattern, addr):
                    addr = normalize(re.sub(r"^(" + pattern + ")(.*)$", r"\2 \1", addr))
                    break
        info["address"] = addr
        return info
    
    # find known prefix
    prefix_pos = None
    found_prefix = None
    for prefix in known_addr_prefixes:
        pos = addr.find(prefix)
        if pos != -1 and pos < header_pos:
            if (pos == 0 and addr[pos + len(prefix)] not in string.letters) \
                or (pos + len(prefix) == len(addr) and addr[pos - 1] not in string.letters) \
                or (addr[pos - 1] not in string.letters and addr[pos + len(prefix)] not in string.letters):
                # starts with known prefix
                if prefix_pos is None or pos < prefix_pos:
                    prefix_pos, found_prefix = pos, prefix
                    if pos == 0: break
    unknown_prefix = ""
    if prefix_pos is not None:
        unknown_prefix, addr = addr[:prefix_pos], addr[prefix_pos:]
        # Move known prefix part to the end of address
        # For example: Suite 120 652 Independence Parkway => 652 Independence Parkway Suite 120
        addr = normalize(re.sub(r"^(" + found_prefix + "\W*?\S+)(.*)$",r"\2 \1", addr))
        
    else:
        # no known prefix found
        unknown_prefix, addr = addr[:header_pos], addr[header_pos:]
    # deal with unknown prefix
    if unknown_prefix:
        if not is_person(unknown_prefix):
            info["company"], unknown_prefix = normalize(unknown_prefix), ""
            while info["company"].endswith(","): info["company"] = info["company"][:-1].strip()
    unknown_prefix = normalize(unknown_prefix)
    while unknown_prefix.endswith(","): unknown_prefix = unknown_prefix[:-1].strip()
    info.update(address=normalize(addr), prefix=normalize(unknown_prefix))
    return info
    
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
        tail = get_tail(page, v)
        info[k] = normalize(get_head(tail, end_marker)) if tail and end_marker in tail else None
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
                       lambda **d: " ".join((d.get('lastname') or '', " %s" % d['firstname'][0] if d.get('firstname') else '',
                                                                     " %s" % d['middlename'][0] if d.get('middlename') else '')),
                       lambda **d: " ".join((d.get('lastname') or '', " %s" % d['firstname'][0] if d.get('firstname') else '')),
                       lambda **d: " ".join((d.get('lastname') or '', " %s" % d['middlename'][0] if d.get('middlename') else '')),
                       lambda **d: " ".join((d.get('lastname') or '', "%s%s" % (d['middlename'][0] if d.get('middlename') else '',
                                                                                d['firstname'][0] if d.get('firstname') else ''))),
                       lambda **d: " ".join((d.get('lastname') or '', "%s%s" % (d['firstname'][0] if d.get('firstname') else '',
                                                                                d['middlename'][0] if d.get('middlename') else ''))),
                      )
    return any(map(lambda fn_factory: smart_cmp(fn_factory(**person), fullname_variant), fullname_factories))

def smart_match_fullname(text, **person):
    """ Returns True if person's name is in the text provided """
    if smart_fullname_cmp(text, **person):
        return True

    text = text.upper()
    for _ in '.,()"\':0123456789!@#$^%&*_~`</>\\': text = text.replace(_," ")
    all_tokens = filter(None, text.split()) 
    tokens_variants = filter(lambda _: len(_) > 1, set(map(tuple, (all_tokens, filter(lambda _: len(_) > 1, all_tokens)))))
    for tokens in tokens_variants:
        for j in xrange(0, len(tokens)):
            pieces = tokens[j:]
            if pieces:
                possible_names = set(" ".join(pieces[:_]) for _ in xrange(2, len(pieces) + 1))
                for _name in possible_names:
                    if smart_fullname_cmp(_name, **person):
                        return True
    return False
