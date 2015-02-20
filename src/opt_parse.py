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


	def parse(self, c = None):
		# \-+\w+=|\w+=
		# content = re.sub('\-+\w+=|\w+=', '=', c).split()

		content = (sys.args if (c == None) else c.split())

		option_input = []
		tmp = []
		focus = None
		cmd_range = []

		# print content

		# print self.opt_hash

		counter = 0
		master_indices = []

		# print self.opt_hash

		for item in content:
			print item
			for master in self.opt_hash:
				if item in self.opt_hash[master][__ALIASES__]:
					master_indices.append(counter)
			counter += 1

		print master_indices

		# print self.opt_hash
		return


		# This piece of code breaks the input up into sub-master command strings to be handled
		# one at a time.
		#
		for mi, item in enumerate(content):
			if item in self.masters:
				tmp.append(mi)

		for first in tmp:
			if (first + 1) >= len(tmp):
				cmd_range.append((tmp[-1], len(content)))
				break
			cmd_range.append((tmp[first], tmp[first + 1]))
		
		for master in cmd_range:
			start = master[0]
			end = master[-1]

			tmp_cut = content[start:end]
			tmp_opt = { 'self' : content[start] }

			print "%s Heloo" % tmp_cut


			for i in range(0, len(tmp_cut)):
				can = tmp_cut[i]
				par = self.opt_hash[tmp_opt['self']]

				if can in par[1]:
					if par[0] == __PREFIX__:
						# TODO: Check if the next field isn't missing. If it is, throw error.
						#  Also check that it is in fact a valid data field (not another command)
						tmp_opt[can] = tmp_cut[i + 1]
					elif par[0] == __FIELD__:
						# TODO: See above
						tmp_opt[self.make_raw(can)] = tmp_cut[i  + 1]
					elif par[0] == __VALUE__:
						tmp_opt[self.make_raw(can)] = True
						pass

			option_input.append(tmp_opt)
						
					

			# for i, cmd in enumerate(tmp_cut):
			# 	if tmp_cut[i] in (self.opt_hash[tmp_cut[0]]):
			# 		print tmp_cut[i]


			# print 
		print option_input
		return

		for idx, master in enumerate(content):
			tmp_opt = {'self':master} # Put all stuff in here
			s_idx = idx
			e_idx = -1

			for run, n in enumerate(content, start=idx):
				if n in self.masters or n == None:
					e_idx = run
					break

			print s_idx, e_idx

			# print idx, val
		return

		index = 0
		while content: # Stops if list is empty
			tmp_opt = {}
			tmp = content.pop(0)

			if tmp in self.masters:
				if focus == None:
					# Means it's the first master level command
					focus = tmp
					tmp_opt['self'] = 'focus'
				
					# Means it's the next master level command
					option_input.append(tmp_opt) # Add the option hash to the list
				index += 1
				continue

			if tmp in self.opt_hash[focus]:
				print "YAY! I found: '" + tmp + "' at index %i" % index
			index += 1

		print option_input



		# COMMAND copy /some/file -t /var/www connect nuclear -u root -t /var/www
		# 
		#
		#

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
		print sub + ": " + data

	def copy(self, master, sub, data):
		pass

if __name__ == "__main__":
	t = Test()
