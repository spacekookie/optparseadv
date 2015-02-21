# =========================================================
# Copyright: (c) 2015 Katharina Sabel
# License  : LGPL 3.0 (See LICENSE)
# Comment  : Main class and body of the advanced options 
#			 parser. See test script for usage info.
# =========================================================

# Some imports
import itertools
import warnings
import console
import re

# Some variables to be used.
__VALUE__ = '__VALUE__'
__PREFIX__ = '__PREFIX__'
__FIELD__ = '__FIELD__'

# Indicates that a master command can have a 1 to 1 binding
# to another parameter afterwards.
__SLAVE__ = '__slave__'

# Values to be used in the options tree
__ALIASES__ = '__alias__'
__FUNCT__ = '__funct__'
__DATAFIELD__ = '__defdat__'
__TYPE__ = '__type__'

# Main class
#
class OptParseAdv:

	def __init__(self, masters = None):
		self.set_masters(masters)
		self.slaves = None
		self.debug = False

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
			self.set_master_field(key, False)

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
	def add_suboptions(self, master, data):
		if master not in self.opt_hash: self.opt_hash[master] = {}
		
		for key, value in data.iteritems():
			if key not in self.opt_hash[master]: self.opt_hash[master][key] = {}
			self.opt_hash[master][key][__ALIASES__] = [key]
			self.opt_hash[master][key][__TYPE__] = value[1]
			self.opt_hash[master][key][__DATAFIELD__] = value[0]

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


	# Allow a master command to bind to a slave field.
	def set_master_field(self, master, slave):
		self.opt_hash[master][__SLAVE__] = slave

	# Added for Poke server handling.
	def define_slaves(self, slaves):
		if self.slaves == None: self.slaves = {}
		for key, value in slaves.iteritems():
			if key not in self.slaves: self.slaves[key] = {}
			self.slaves[key] = value

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
			self.opt_hash[master][key][__ALIASES__] += value

	# Enables debug mode on the parser.
	# Will for example output the parsed and translated/ chopped strings to the console.
	#
	def enable_debug(self):
		self.debug = True

	# Parse a string either from a method parameter or from a commandline
	# argument. Calls master command functions with apropriate data attached
	# to it.
	#
	def parse(self, c = None):
		# \-+\w+=|\w+=
		# content = re.sub('\-+\w+=|\w+=', '=', c).split()
		# print self.opt_hash

		content = (sys.args if (c == None) else c.split())
		counter = 0
		master_indices = []
		focus = None

		if self.debug: print "['%s']" % c, "==>", content

		for item in content:
			# print item
			for master in self.opt_hash:
				if item in self.opt_hash[master][__ALIASES__]:
					master_indices.append(counter)
			counter += 1

		counter = 0
		skipper = False
		wait_for_slave = False
		master_indices.append(len(content))
		# print master_indices

		# This loop iterates over the master level commands
		# of the to-be-parsed string
		for index in master_indices:
			if (counter + 1) < len(master_indices):
				# print (counter + 1), len(master_indices)
				data_transmit = {}
				subs = []
				sub_counter = 0
				slave_field = None
				has_slave = False

				# This loop iterates over the sub-commands of several master commands.
				#
				for cmd in itertools.islice(content, index, master_indices[counter + 1] + 1):
					if sub_counter == 0:
						focus = self.__alias_to_master(cmd)
						if focus in self.opt_hash:
							if self.opt_hash[focus][__SLAVE__]:
								wait_for_slave = True
								sub_counter += 1
								continue

					else:
						rgged = cmd.replace('=', '= ').split()

						for sub_command in rgged:
							if skipper: 
								skipper = False
								continue

							if "=" in sub_command:
								sub_command = sub_command.replace('=', '')
								trans_sub_cmd = self.__alias_to_sub(focus, sub_command)

								if trans_sub_cmd in self.opt_hash[focus]:
									data_transmit[trans_sub_cmd] = rgged[1]
									skipper = True
									if trans_sub_cmd not in subs: subs.append(trans_sub_cmd)
							else:
								if wait_for_slave:
									has_slave = True
									wait_for_slave = False
									if sub_command in self.slaves:
										slave_field = (sub_command, self.slaves[sub_command])
									else:
										print "CRITICAL ERROR!"
									continue

								trans_sub_cmd = self.__alias_to_sub(focus, sub_command)
								if trans_sub_cmd == None:
									if sub_command in self.opt_hash:
										if self.opt_hash[sub_command][__SLAVE__]:
											# if self.debug: print "Waiting for slave field..."
											wait_for_slave = True
											continue


								if trans_sub_cmd in self.opt_hash[focus]:
									data_transmit[trans_sub_cmd] = True
									if trans_sub_cmd not in subs: subs.append(trans_sub_cmd)

					sub_counter += 1
				self.opt_hash[focus][__FUNCT__](focus, slave_field, subs, data_transmit)
			counter += 1

	def help_screen(self):
		(width, height) = console.getTerminalSize()
		if self.debug: print "Your terminal's width is: %d" % width

	def print_debug(self):
		print self.opt_hash

	def __alias_to_master(self, alias):
		for master in self.opt_hash:
			for alias_list in self.opt_hash[master][__ALIASES__]:
				if alias in alias_list:
					return master
		return None

	def __alias_to_sub(self, master, alias):
		for sub in self.opt_hash[master]:
			if "__" not in sub:
				if alias in self.opt_hash[master][sub][__ALIASES__]:
					return sub
		return None



#########################
#   TEST SCRIPT BELOW   #
#########################


# [Master Command] [ Slave Field (if not None) ] [ List of Sub Commands ] [ Sub command data hash ]
# 
#
# def connect(master, slave, sub, data):
# 	print master, slave, sub, data

# def copy(master, slave, sub, data):
# 	pass #print master, "This is a copy with", sub, "and", data

# p = OptParseAdv({'connect':connect})
# # p.enable_debug()

# p.set_master_field('connect', True)
# p.master_aliases('connect', ['c'])

# p.define_slaves({'nas':'192.168.2.131'})

# p.add_suboptions('connect', {'-X': (None, __VALUE__), '--command': (None, __FIELD__)})
# # p.add_suboptions('copy', {'--file': (None, __FIELD__)})
# p.sub_aliases('connect', {'-X': ['-X'], '--command': ['-c']})
# # p.sub_aliases('copy', {'--file': ['-f']})


# # p.print_debug()

# p.parse('c nas -X')