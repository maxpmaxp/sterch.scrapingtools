### -*- coding: utf-8 -*- #############################################
# Разработано компанией Стерх (http://sterch.net/)
# Все права защищены, 2008
#
# Developed by Sterch (http://sterch.net/)
# All right reserved, 2008
#######################################################################

""" Headers dictionary

$Id: headers.py 14192 2010-04-17 08:44:49Z maxp $
"""
__author__  = "Polscha Maxim (maxp@sterch.net)"
__license__ = "<undefined>" # необходимо согласование
__version__ = "$Revision: 14192 $"
__date__ = "$Date: 2010-04-17 11:44:49 +0300 (Сб, 17 апр 2010) $"

from random import choice, randint
from copy import copy
import string

browser_headers = [
 [
                   ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/532.0 (KHTML, like Gecko) Chrome/3.0.195.21 Safari/532.0'),
                   ('Accept', 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'),
                   ('Accept-Language', 'en-US;q=0.8,en;q=0.6'),
                   ('Accept-Charset', 'utf-8;q=0.8,latin-1;q=0,6,*;q=0.3'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) (KHTML, like Gecko)'),
                   ('Accept', 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'),
                   ('Accept-Language', 'en-US'),
                   ('Accept-Charset', 'utf-8;q=0.9,latin-1;q=0,7,*;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; uk; rv:1.9.1.3) Gecko/20090824 Firefox/3.5.3 GTB5 (.NET CLR 3.5.30729)'),
                   ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,text/vnd.wap.wml;q=0.6'),
                   ('Accept-Language', 'ru,uk;q=0.8,en;q=0.7,de;q=0.5,ru-ru;q=0.3,en-us;q=0.2'),
                   ('Accept-Charset', 'utf-8;q=0.8,*;q=0.7'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru-RU) AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19.1'),
                   ('Accept', 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'),
                   ('Accept-Language', 'en-US'),
                   ('Accept-Charset', 'iso-8859-1, utf-8'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Opera/9.80 (Windows NT 5.1; U; en)'),
                   ('Accept', 'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1'),
                   ('Accept-Language', 'en;q=0.9,ru;q=0.1'),
                   ('Accept-Charset', 'iso-8859-1, utf-8, utf-16, *;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Opera/9.80 (Windows NT 5.1; U; en) Presto/2.2.15 Version/10.00'),
                   ('Accept', 'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1'),
                   ('Accept-Language', 'en-US,en;q=0.9,en;q=0.8'),
                   ('Accept-Charset', 'iso-8859-1, utf-8, utf-16, *;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'),
                   ('Accept', 'image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, application/x-silverlight, application/x-ms-application, application/x-ms-xbap, application/vnd.ms-xpsdocument, application/xaml+xml, */*'),
                   ('Accept-Language', 'ru,en-US;q=0.5'),
                   ('Accept-Charset', 'iso-8859-1, utf-8, utf-16, *;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)'),
                   ('Accept', 'image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, application/x-silverlight, application/x-ms-application, application/x-ms-xbap, application/vnd.ms-xpsdocument, application/xaml+xml, */*'),
                   ('Accept-Language', 'en-US;q=0.9'),
                   ('Accept-Charset', 'iso-8859-1, utf-8, utf-16, *;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'),
                   ('Accept', 'image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, application/x-silverlight, application/x-ms-application, application/x-ms-xbap, application/vnd.ms-xpsdocument, application/xaml+xml, */*'),
                   ('Accept-Language', 'en-US;q=0.7'),
                   ('Accept-Charset', 'iso-8859-1, utf-8, utf-16, *;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) (KHTML, like Gecko)'),
                   ('Accept', 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5'),
                   ('Accept-Language', 'en-US'),
                   ('Accept-Charset', 'utf-8;q=0.8,iso-8859-1;q=0.6,*;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/5.0 (Windows; Windows NT 5.1; US; rv:1.9.1) Gecko/20090720 Firefox/3.5.1'),
                   ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.8,*/*;q=0.4,text/vnd.wap.wml;q=0.2'),
                   ('Accept-Language', 'en;q=0.7,en-us;q=0.2'),
                   ('Accept-Charset', 'utf-8, iso-8859-1;q=0.8,*;q=0.6'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/5.0 (Windows NT 5.1; en-US) AppleWebKit/530.19.2 Version/4.0.1 Safari/530.17.0'),
                   ('Accept', 'application/xml,application/xhtml+xml,text/html;q=0.8,text/plain;q=0.7,image/png,*/*;q=0.1'),
                   ('Accept-Language', 'en-US, en;q=0.9'),
                   ('Accept-Charset', 'utf-8, iso-8859-1;q=0.9'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Opera/9.85 (Windows NT 5.1; en-US)'),
                   ('Accept', 'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1'),
                   ('Accept-Language', 'en;q=0.9'),
                   ('Accept-Charset', 'iso-8859-1, utf-8;q=0.5, utf-16, *;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Opera/9.88 (Windows NT 5.1; en) Presto/2.1.13 Version/9.00'),
                   ('Accept', 'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1'),
                   ('Accept-Language', 'en-US;q=0.9,en;q=0.3'),
                   ('Accept-Charset', 'iso-8859-1, utf-8;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50700;'),
                   ('Accept', 'image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, application/x-silverlight, application/x-ms-application, application/x-ms-xbap, application/vnd.ms-xpsdocument, application/xaml+xml, */*'),
                   ('Accept-Language', 'en-US;q=0.8'),
                   ('Accept-Charset', 'iso-8859-1, utf-8;q=0.4'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/3.9)'),
                   ('Accept', 'image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, application/x-silverlight, application/x-ms-application, application/x-ms-xbap, application/vnd.ms-xpsdocument, application/xaml+xml, */*'),
                   ('Accept-Language', 'en-US;q=0.9'),
                   ('Accept-Charset', 'iso-8859-1, utf-8, *;q=0.3'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1;  .NET CLR 2.0.507123;)'),
                   ('Accept', 'image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, application/x-silverlight, application/x-ms-application, application/x-ms-xbap, application/vnd.ms-xpsdocument, application/xaml+xml, */*'),
                   ('Accept-Language', 'en,en-US;q=0.7'),
                   ('Accept-Charset', 'iso-8859-1, utf-8;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
  [                 
                   ('User-Agent', 'Opera/9.65 (Windows; Windows NT 5.1; en) Version/9.00'),
                   ('Accept', 'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1'),
                   ('Accept-Language', 'en-US;q=0.9,en;q=0.3'),
                   ('Accept-Charset', 'iso-8859-1, utf-8;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows; Windows NT 5.1; .NET'),
                   ('Accept', 'image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, application/x-silverlight, application/x-ms-application, application/x-ms-xbap, application/vnd.ms-xpsdocument, application/xaml+xml, */*'),
                   ('Accept-Language', 'en-US;q=0.9'),
                   ('Accept-Charset', 'iso-8859-1, utf-8;q=0.4'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/3.7; .NET)'),
                   ('Accept', 'image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, application/x-silverlight, application/x-ms-application, application/x-ms-xbap, application/vnd.ms-xpsdocument, application/xaml+xml, */*'),
                   ('Accept-Language', 'en-US;q=0.9'),
                   ('Accept-Charset', 'iso-8859-1, utf-8, *;q=0.3'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Mozilla/4.0 (compatible; MSIE 7.0; Windows; Windows NT 5.1; US)'),
                   ('Accept', 'image/gif, image/jpeg, image/pjpeg, image/pjpeg, application/x-shockwave-flash, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, application/x-silverlight, application/x-ms-application, application/x-ms-xbap, application/vnd.ms-xpsdocument, application/xaml+xml, */*'),
                   ('Accept-Language', 'en,en-US;q=0.7'),
                   ('Accept-Charset', 'iso-8859-1, utf-8;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Opera/9.68 (Windows; Windows; Windows NT 5.1; en)'),
                   ('Accept', 'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1'),
                   ('Accept-Language', 'en-US;q=0.9,en;q=0.3'),
                   ('Accept-Charset', 'iso-8859-1, utf-8;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Opera/9.68 ( Windows NT 5.1; en) Version/9.00'),
                   ('Accept', 'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1'),
                   ('Accept-Language', 'en-US;q=0.9,en;q=0.3'),
                   ('Accept-Charset', 'iso-8859-1, utf-8;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
 [                 
                   ('User-Agent', 'Opera/9.67 (Windows; Windows NT 5.1; en) Version/9.00'),
                   ('Accept', 'text/html, application/xml;q=0.9, application/xhtml+xml, image/png, image/jpeg, image/gif, image/x-xbitmap, */*;q=0.1'),
                   ('Accept-Language', 'en-US;q=0.9,en;q=0.3'),
                   ('Accept-Charset', 'iso-8859-1, utf-8;q=0.1'),
                   ('Keep-Alive', '300'),
                   ('Connection', 'keep-alive')
 ],
]

def getheaders():
    """ Returns random browser headers """
    headers = copy(choice(browser_headers))
    ua, value = headers[0]
    name = "".join([choice(string.letters) for l in xrange(0,randint(3,10))])
    major = str(randint(0,9))
    middle =  str(randint(0,20))
    minor =  str(randint(0,150))
    tail = "; %s v%s.%s.%s;" % (name, major, middle, minor)
    index = value.find(")")
    if index > 0:
        value = value[:index] + tail + value[index:]  
    else:
        value = value + tail
    headers[0] = (ua, value)
    headers.append(("X-Forwarded-For", ".".join(map(str,[10,randint(0,253),randint(0,253),randint(1,253)]))))
    
    return headers 