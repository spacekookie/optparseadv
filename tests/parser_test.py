# =========================================================
# Copyright: (c) 2015 Katharina Sabel
# License  : LGPL 3.0 (See LICENSE)
# Comment  : Testing script for options parser
#
# =========================================================

# Prepare application path
import sys
sys.path.append('../lib/')

import adv_opt_parse as parser

def connect(master, slave, sub, data):
	print master, slave, sub, data

p = parser.OptParseAdv({'connect':connect})
p.set_master_field('connect', True)
p.master_aliases('connect', ['c'])
p.define_slaves({'nas':'192.168.2.131'})
p.add_suboptions('connect', {'-X': (None, parser.__VALUE__), '--command': (None, parser.__FIELD__)})
p.sub_aliases('connect', {'-X': ['-X'], '--command': ['-c']})

p.parse('c nas -X')