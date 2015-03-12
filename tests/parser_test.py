"""
Test script
===========

:copyright: (C) 2015 Katharina Sabel <SpaceKookie>
:license: GPLv2 (See LICENSE)
"""

from advoptparse import parser as p

# This function will be called when input is parsed correctly
def handler(master, field, sub, data):
	print master, field, sub, data

parser = p.AdvOptParse({'func': (handler, 'Description of a function')})

# Set up some basic data about the container application
p.set_container_name("app")
p.set_container_version("1.0")
p.define_version_handle(['-ver'])

# Make the 'function' argument accept fields
p.set_master_fields('func', True)

# Give it an alias to make typing it more convenient for users
p.set_master_aliases('func', ['func'])

# Give the master command some sub argument fields to be handled
p.add_suboptions('func', {'-k': (None, p.__VALUE__, "Some description")})
p.add_suboptions('func', {'--file': (None, p.__FIELD__, "Use parameters")})


# Parse something, envelopped in a try-except block
# to handle failures to container applications
try:
	p.parse('f -k --file=some/file.txt')
except:
	print "Input not valid"
	parser.help_screen()