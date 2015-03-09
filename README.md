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

```
python

	import adv_opt_parse as parse

	def connect(master, fields, sub, data):
		print master, fields, sub, data

	def copy(master, sub, data):
		print "This is a copy with", sub, "and", data

	p = parse.OptParseAdv({'connect':connect,'copy':copy})
	# p.enable_debug()
	p.add_suboptions('copy', {'--file': (None, parse.__FIELD__), '--target': ('~/poke', parse.__FIELD__)})
	p.sub_aliases('copy', {'--target': ['-t'], '--file': ['-f']})
	p.master_aliases('copy', ['cp'])
	p.parse('connect cp -f=/foo/bar.poo -t=/foo')
```
