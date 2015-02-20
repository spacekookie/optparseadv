import adv_opt_parse as parse

def connect(master, sub, data):
	print "This is a connect to", sub, "with data", data

def copy(master, sub, data):
	print "This is a copy with", sub, "and", data

p = parse.OptParseAdv({'connect':connect,'copy':copy})
# p.enable_debug()
p.add_suboptions('copy', {'--file': (None, parse.__FIELD__), '--target': ('~/poke', parse.__FIELD__)})
p.sub_aliases('copy', {'--target': ['-t'], '--file': ['-f']})
p.master_aliases('copy', ['cp'])
p.parse('connect cp -f=/foo/bar.poo -t=/foo')