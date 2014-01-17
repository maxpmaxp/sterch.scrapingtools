### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012, 2013
#######################################################################

""" Fullname parsing utilities. Internal use only.
"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

lastname_prefixes = ('MC', 'VAN')

def parse_lfms(allnames):
    """ Groups allnames list according to lfms schema """
    job = dict()
    if len(allnames) == 2:
         job['lastname'] = allnames[0]
         job['firstname'] = allnames[1]
    elif len(allnames) > 2:
        if allnames[0].upper() not in lastname_prefixes:
            job['lastname'] = allnames[0]
            job['firstname'] = allnames[1]
            job['middlename'] = " ".join(allnames[2:])
        else:
            job["lastname"] = "%s %s" % (allnames[0], allnames[1])
            job['firstname'] = allnames[2]
            job['middlename'] = " ".join(allnames[3:])
    return job

def parse_lmfs(allnames):
    """ Groups allnames list according to lmfs schema """
    job = dict()
    if len(allnames) == 2:
         job['lastname'] = allnames[0]
         job['firstname'] = allnames[1]
    elif len(allnames) > 2:
        if allnames[0].upper() not in lastname_prefixes:
            job['lastname'] = allnames[0]
            job['firstname'] = allnames[-1]
            job['middlename'] = " ".join(allnames[1:-1])
        else:
            job["lastname"] = "%s %s" % (allnames[0], allnames[1])
            job['firstname'] = allnames[-1]
            job['middlename'] = " ".join(allnames[2:-1])
    return job
    
def parse_fmls(allnames):
    """ Groups allnames list according to fmls schema """
    job = dict()
    if len(allnames) == 2:
        job['firstname'] = allnames[0]
        job['lastname'] = allnames[1]
    elif len(allnames) > 2:
        job['firstname'] = allnames[0]
        if allnames[-2].upper() not in lastname_prefixes: 
            job['lastname'] = allnames[-1]
            job['middlename'] = " ".join(allnames[1:-1])
        else:
            job['lastname'] = "%s %s" % (allnames[-2], allnames[-1])
            job['middlename'] = " ".join(allnames[1:-2])
    return job

def parse_flms(allnames):
    """ Groups allnames list according to flms schema """
    job = dict()
    if len(allnames) == 2:
        job['firstname'] = allnames[0]
        job['lastname'] = allnames[1]
    elif len(allnames) > 2:
        if allnames[1].upper() not in lastname_prefixes:
             job['firstname'] = allnames[0]
             job['lastname'] = allnames[1]
             job['middlename'] = " ".join(allnames[2:])
        else:
            job['firstname'] = allnames[0]
            job['lastname'] = "%s %s" % (allnames[1], allnames[2])
            job['middlename'] = " ".join(allnames[3:])
    return job