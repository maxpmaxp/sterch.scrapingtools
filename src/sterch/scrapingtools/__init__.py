### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2008
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2008
#######################################################################
# $Id: __init__.py 14592 2010-05-17 11:00:42Z maxp $
#######################################################################

# Make it a Python package
from opener import createOpener, readpage, proxies, Client, BaseCaptchaAwareClient
from output import start_chunked_stdout, stop_chunked_stdout
from queue import pickleQueue, unpickleQueue, processQueue, SyncList, DuplicateValueError
from queue import DumpingGetQueue, DumpingPutQueue
from text import replace_html_entities, striptags, normalize, tofilename
from writer import CSVWriter, SimpleCSVWriter
from worker import Worker, workers_group_factory, filter_dead_workers