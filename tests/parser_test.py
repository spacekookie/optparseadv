# =========================================================
# Copyright: (c) 2015 Katharina Sabel
# License  : LGPL 3.0 (See LICENSE)
# Comment  : Testing script for options parser
#
# =========================================================

# Prepare application path
import sys
sys.path.append('../src/')

import adv_opt_parse as parser

def connect(master, sub, data):
	pass
	# print "This is a connect to", sub, "with data", data

def copy(master, sub, data):
	pass
	# print "This is a copy with", sub, "and", data

p = parser.OptParseAdv({'connect':connect, 'copy':copy})
# p.enable_debug()
p.add_suboptions('connect', {'-X': (None, parser.__VALUE__)})
p.add_suboptions('copy', {'--file': (None, parser.__FIELD__)})

p.sub_aliases('connect', {'-X': ['-X']})
p.sub_aliases('copy', {'--file': ['-f', '--file']})
p.master_aliases('connect', ['c'])

p.parse('copy --file=/path/to/file')