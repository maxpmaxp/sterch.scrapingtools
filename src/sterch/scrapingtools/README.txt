Library to build scrapers.
Property of Sterch ltd. http://sterch.net/
Author: Polscha Maxim (maxp@sterch.net)

Requires Python >= 2.5.4

CONFIGURATION
	1. config.py has following configurable variables:
		
		* MAXREADTRIES --- max. number of url read tries. Value of 2 looks usable.
		* DELAY --- delay between threads checks.
		
	   
	2. You can define list of proxies to use in the file proxies.txt. 
	   Lines starts with # are comments.

	3. You can define list of IPs to use in the file ips.txt. 
	   Lines starts with # are comments.
