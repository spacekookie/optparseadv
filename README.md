Python options parser
==========

This is a library that provices enhanced functionality to python by adding a parser for commandline arguments, including but not limited to options (e.g. '-v'), data fields (e.g. 'file=/path/to/file') as well as sub-command fields ands scopes (e.g.'git clone')

It also adds support for chaining commands and options such as they are being executed sequentially. (e.g. 'git add * commit -m "Some message" push)

## How to use

```python


	# Sets up the parser with it's master level commands 'connect' and 'copy' 
	# bound to the functions 'self.connect' and 'self.copy'
	p = OptParseAdv(self, {'connect':self.connect,'copy':self.copy})
	
	# Add suboptions for copy with a hash and their default usage to FIELD
	p.add_suboptions('copy', {'--file': (None, __FIELD__), '--target': ('~/poke', __FIELD__)})

	# Add aliases for both '--target'and '--file'
	p.sub_aliases('copy', {'--target': ['-t'], '--file': ['-f']})
	
	# Add alise for copy
	p.master_aliases('copy', ['cp'])

	# Use all of that to parse a lovely string.
	p.parse('cp -f=/foo/bar.poo -t=/foo connect')


```