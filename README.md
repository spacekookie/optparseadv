Python options parser
==========

This is a library that provices enhanced functionality to python by adding a parser for commandline arguments, including but not limited to options (e.g. '-v'), data fields (e.g. 'file=/path/to/file') as well as sub-command fields ands scopes (e.g.'git clone')

It also adds support for chaining commands and options such as they are being executed sequentially. (e.g. 'git add * commit -m "Some message" push)

## How to use

```python

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