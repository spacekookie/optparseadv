# =========================================================
# Copyright: (c) 2015 Katharina Sabel
# License  : GPL 2.0 (See LICENSE)
# Comment  : Testing script for options parser
#
# =========================================================

import sys
import unittest

sys.path.append('../src/')
import adv_opt_parse as parser

def fun(x):
	return x + 1

class ParserTest(unittest.TestCase):

	def test(self):
		# p = parser.OptParseAdv({'connect':(parity, 'Connect to servers')})
		# p.set_master_fields('connect', True)
		# p.set_master_aliases('connect', ['c'])
		# p.define_fields({'nas':'192.168.2.131'})
		# p.add_suboptions('connect', {'-X': (None, parser.__VALUE__, "Enable X forwarding")})
		
		# p.parse("connect nas -X")
		self.assertEqual(3, 3)