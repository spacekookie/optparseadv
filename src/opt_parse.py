# Copyright (C) 2014 Katharina Sabel
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


# Some imports
import itertools
import warnings
import re


# Some variables to be used.
__VALUE__ = '__VALUE__'
__PREFIX__ = '__PREFIX__'
__FIELD__ = '__FIELD__'

__ALIASES__ = '__alias__'
__FUNCT__ = '__funct__'
__DATAFIELD__ = '__defdat__'
__TYPE__ = '__type__'


# Main class
#
class OptParseAdv:

	def __init__(self, parent, masters = None):
		self.parent = parent #Is this needed?
		self.set_masters(masters)
		self.iterating = False


	# Hash of master level commands. CAN contain a global function to determine actions of
	# subcommands.
	# (See docs).
	#
	def set_masters(self, masters):
		if masters == None: warnings.warn("Warning! You shouldn't init a parser without your master commands set!")
		# self.masters = master
		self.opt_hash = {}
		for key, value in masters.iteritems():
			self.opt_hash[key] = {}
			self.opt_hash[key][__FUNCT__] = value
			self.master_aliases(key, [])

	# Takes the master level command and a hash of data
	# The hash of data needs to be formatted in the following sense:
	# {'X': funct} where X is any variable, option or command INCLUDING DASHES AND DOUBLE DASHES you want
	# to add to your parser.
	# Additionally you pass a function from your parent class that gets called when this option is detected in a
	# string that is being parsed. The function by detault takes three parameters: 
	# 
	# master command (i.e. copy), parent option (i.e. '-v'), data field default (i.e. 'false'). So in an example for
	#
	# "clone -L 2"
	#
	# it would call the function: func('clone', '-L', '2') in the specified container class/ env.
	#
	# 'use' parameters include:	'value'	: -v
	# 							'prefix': --logging true
	#							'field'	: --file=/some/data
	#
	# 
	def add_suboptions(self, master, data):
		if master not in self.opt_hash: self.opt_hash[master] = {}
		
		for key, value in data.iteritems():
			if key not in self.opt_hash[master]: self.opt_hash[master][key] = {}
			self.opt_hash[master][key][__ALIASES__] = []
			self.opt_hash[master][key][__TYPE__] = value[1]
			self.opt_hash[master][key][__DATAFIELD__] = value[0]

		# print self.opt_hash
		# if data[0] not in self.opt_hash[master]: self.opt_hash[master][data[0]] = (data[1], use)

	# Create aliases for a master command that invoke the same
	# functions as the actual master command.
	# 
	# This can be used to shorten commands that user need to
	# input (such as 'rails server' vs 'rails s' does it)
	#
	def master_aliases(self, master, aliases):
		if master not in self.opt_hash: warnings.warn("Could not identify master command. Aborting!") ; return
		if master not in aliases: aliases.append(master)
		self.opt_hash[master][__ALIASES__] = aliases
		# print self.opt_hash

	# Create aliases for a sub command that invoke the same
	# functions as the actual sub command.
	# 
	# This can be used to shorten commands that user need to
	# input (such as 'poke copy --file' vs 'poke copy -f')
	#
	# Can be combined with master alises to make short and nicely
	# cryptic commands:
	# poke server cp -f=~/file -t=directory/ 
	#
	# == USAGE ==
	# Specify the master level command as the first parameter.
	# Then use a hash with the original subs as the indices and
	# the aliases in a list as values. This allows for ALL aliases for
	# a master level command to be set at the same time without having
	# to call this function multiple times.
	#
	def sub_aliases(self, master, aliases):
		if master not in self.opt_hash: warnings.warn("Could not identify master command. Aborting!") ; return

		for key, value in aliases.iteritems():
			if key not in self.opt_hash[master]: warnings.warn("Could not identify sub command. Skipping") ; continue
			self.opt_hash[master][key][__ALIASES__] = value

		# print self.opt_hash[master]

	def make_raw(self, string):
		return string.replace('-', '')

	def alias_to_master(self, alias):
		for master in self.opt_hash:
			for alias_list in self.opt_hash[master][__ALIASES__]:
				if alias in alias_list:
					return master
		return None

	def alias_to_sub(self, master, alias):
		for sub in self.opt_hash[master]:
			if "__" not in sub:
				if alias in self.opt_hash[master][sub][__ALIASES__]:
					return sub
		return None

		return
		for sub in self.opt_hash[master]:
			for alias_list in self.opt_hash[master][sub][__ALIASES__]:
				if alias in alias_list:
					return sub


	def parse(self, c = None):
		# \-+\w+=|\w+=
		# content = re.sub('\-+\w+=|\w+=', '=', c).split()

		content = (sys.args if (c == None) else c.split())
		counter = 0
		master_indices = []
		cmd_tree = {}
		focus = None

		# print self.opt_hash
		print content

		for item in content:
			# print item
			for master in self.opt_hash:
				if item in self.opt_hash[master][__ALIASES__]:
					master_indices.append(counter)
			counter += 1

		#print master_indices

		counter = 0
		for index in master_indices:
			if (counter + 1) < len(master_indices):
				#print "Crnt is ==>", index
				#print "Next is ==>", master_indices[counter + 1]
				sub_counter = 0
				for cmd in itertools.islice(content, index, master_indices[counter + 1]):
					if sub_counter == 0:
						focus = self.alias_to_master(cmd)
						cmd_tree[focus] = {}
					else:
						if "=" in cmd:
							rgged = cmd.replace('=', ' ').split()
							for sub_command in rgged:
								trans_sub_cmd = self.alias_to_sub(focus, sub_command)
								if trans_sub_cmd in self.opt_hash[focus]:
									print "'%s'" % rgged[1], "combined with", trans_sub_cmd
									call = self.opt_hash[focus][__FUNCT__]
									call(focus, trans_sub_cmd, None)

						# print cmd
					sub_counter += 1
				# print "\n", cmd_tree, "\n"
			else:
				print "No next. Last is", counter
				break
			counter += 1

		print "EX MOTHERFUCKING CELSIOR!"

class Test:

	def __init__(self):
		p = OptParseAdv(self, {'connect':self.connect,'copy':self.copy}) # Sets up the master level commands to connect and copy
		p.add_suboptions('copy', {'--file': (None, __FIELD__), '--target': ('~/poke', __FIELD__)})
		p.sub_aliases('copy', {'--target': ['-t'], '--file': ['-f']})
		p.master_aliases('copy', ['cp'])

		p.parse('cp -f=/foo/bar.poo -t=/foo connect')
		# p.add_suboptions('connect', ('-t', None), use='prefix')
		# p.add_suboptions('copy', ('--file', None), use=__FIELD__)
		# p.add_suboptions('copy', ('--target', None), use=__FIELD__)
		# p.parse("copy --file=/path/to/file --target=~/Documents/ ")

	def connect(self, master, sub, data):
		print "YES IT WORKS"
		print sub + ": " + data

	def copy(self, master, sub, data):
		print "FUCK YES FUCK FUCK FUCK!!!"
		pass

if __name__ == "__main__":
	t = Test()

