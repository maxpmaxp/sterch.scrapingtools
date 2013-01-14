### -*- coding: utf-8 -*- #############################################
# Developed by Maksym Polshcha (maxp@sterch.net)
# All right reserved, 2012
#######################################################################

# Make it a Python package
from opener import createOpener, readpage, Client, BaseCaptchaAwareClient
from output import start_chunked_stdout, stop_chunked_stdout
from synclist import SyncList, DuplicateValueError
from text import replace_html_entities, striptags, normalize, tofilename, parse_fullname, parse_fulladdress
from text import remove_aka, is_person, parse_city_state_zip, normalize_address, is_fullname_suffix
from writer import CSVWriter, SimpleCSVWriter
from worker import Worker, workers_group_factory, filter_dead_workers