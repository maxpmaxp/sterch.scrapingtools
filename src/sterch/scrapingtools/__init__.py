### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012, 2013, 2014,2015
#######################################################################

# Make it a Python package
from courts import is_plaintiff, is_defendant, is_attorney, extract_description, extract_date, extract_money, is_john_doe, is_valid_attorney, SequenceState
from opener import createOpener, Client, clone_client
from output import start_chunked_stdout, stop_chunked_stdout
from synclist import SyncList, DuplicateValueError
from text import replace_html_entities, striptags, normalize, tofilename, parse_fullname, parse_fulladdress
from text import remove_aka, is_person, parse_city_state_zip, normalize_address, is_normal_address, is_fullname_suffix
from text import smart_cmp, smart_fullname_cmp, smart_match_fullname, parse_and_normalize_streetaddress
from text import get_head, get_block, get_tail, walk_table, parse_ff_mapping, US_STATE_CODES, CA_PROVINCE_CODES
from writer import CSVWriter, SimpleCSVWriter
from worker import Worker, workers_group_factory, filter_dead_workers