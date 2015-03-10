Python options parser
==========

This is a library that provices enhanced functionality to python commandline argument handling, including but not limited to options (e.g. '-v'), data fields (e.g. 'file=/path/to/file') as well as chainable sub-commands and scopes (e.g. git commit -m "Message" push) 

AdvOptParse is compatible with Python 2.7 and above.

## How to install
When installing AdvOptParse you have two options. The first one is via pip (or easy_install):
```
$ sudo pip install advoptparse
```

Alternatively you can grab a current source copy of the library via this repository
```
$ git clone -b develop https://github.com/SpaceKookie/AdvOptParse.git
$ cd AdvOptParse/
$ sudo python setup.py install
```
The latter will give you access to the latest development snapshot of the AdvOptParse library.

## How to use

```python
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
	
```

## Support
If you find any bugs with this library or have issues using it, please report them on the github issue tracker. Additonally, if you want to get in contact with me, don't hesitate to e-mail me at katharina.sabel@2rsoftworks.de
