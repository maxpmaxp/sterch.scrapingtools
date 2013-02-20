### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012, 2013
#######################################################################

""" Fullname parsing utilities. Internal use only.
"""
__author__  = "Polshcha Maxim (maxp@sterch.net)"
__license__ = "ZPL"

def parse_lfms(allnames):
    """ Groups allnames list according to lfms schema """
    job = dict()
    if len(allnames) == 2:
         job['lastname'] = allnames[0]
         job['firstname'] = allnames[1]
    elif len(allnames) > 2:
         job['lastname'] = allnames[0]
         job['firstname'] = allnames[1]
         job['middlename'] = " ".join(allnames[2:])
    return job

def parse_lmfs(allnames):
    """ Groups allnames list according to lmfs schema """
    job = dict()
    if len(allnames) == 2:
         job['lastname'] = allnames[0]
         job['firstname'] = allnames[1]
    elif len(allnames) > 2:
         job['lastname'] = allnames[0]
         job['firstname'] = allnames[-1]
         job['middlename'] = " ".join(allnames[1:-1])
    return job
    
def parse_fmls(allnames):
    """ Groups allnames list according to fmls schema """
    job = dict()
    if len(allnames) == 2:
         job['firstname'] = allnames[0]
         job['lastname'] = allnames[1]
    elif len(allnames) > 2:
         job['firstname'] = allnames[0]
         job['lastname'] = allnames[-1]
         job['middlename'] = " ".join(allnames[1:-1])
    return job

def parse_flms(allnames):
    """ Groups allnames list according to flms schema """
    job = dict()
    if len(allnames) == 2:
         job['firstname'] = allnames[0]
         job['lastname'] = allnames[1]
    elif len(allnames) > 2:
         job['firstname'] = allnames[0]
         job['lastname'] = allnames[1]
         job['middlename'] = " ".join(allnames[2:])
    return job
