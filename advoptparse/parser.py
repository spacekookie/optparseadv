# =========================================================
# Copyright: (c) 2015 Katharina Sabel
# License  : GPL 2.0 (See LICENSE)
# Comment  : Main file for the advanced options parser
#
# =========================================================

# Some imports
import itertools
import warnings
import console
import re

# Colour class to make output more pretty.
#
class Colour:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# Some variables to be used.
__VALUE__ = '__VALUE__'
__PREFIX__ = '__PREFIX__'
__FIELD__ = '__FIELD__'

# Indicates that a master command can have a 1 to 1 binding
# to another parameter afterwards.
__BINDING__ = '__bondage__'

# Help handle binding
__HELPER__ = '__helper__'

# Version handle binding
__VERSION__ = '__version__'

# Helper to indicate that a boolean is being stored
__ACTIVE__ = '__kinkysex__'

# Binds an outside function to the failsafe handler.
# Without a bound function a default error message will be
# printed instead.
# => failsafe_function

# Values to be used in the options tree
__ALIASES__ = '__alias__'
__FUNCT__ = '__funct__'
__DATAFIELD__ = '__defdat__'
__TYPE__ = '__type__'

# Notes are used to describe commands
__NOTE__ = '__note__'

# Labels are used to sub-divide master/ sub commands
__LABEL__ = '__label__'

# Main class for the python advanced options parser.
#
class AdvOptParse:

	def __init__(self, masters = None):
		self.__set_masters(masters)
		self.failsafe_function = None
		self.container_name = None
		self.fields_name = "Fields"
		self.slave_fields = None
		self.debug = False

	# Set the name of the container application that's used in the help screen
	#
	def set_container_name(self, name):
		self.container_name = name


	# Set the name of the fields for the help screen
	#
	def set_fields_name(self, name):
		self.fields_name = name


	# Hash of master level commands. CAN contain a global function to determine actions of
	# subcommands.
	# (See docs).
	#
	def __set_masters(self, masters):
		if masters == None: warnings.warn("Warning! You shouldn't init a parser without your master commands set!")
		# self.masters = master
		self.opt_hash = {}
		for key, value in masters.iteritems():
			self.opt_hash[key] = {}
			self.opt_hash[key][__FUNCT__] = value[0]
			self.opt_hash[key][__NOTE__] = value[1]
			self.set_master_aliases(key, [])
			self.set_master_fields(key, False)

		# Setup the version and helper handle. By default '-h' and '--version' are set to 'True'
		self.opt_hash[__HELPER__] = { __ALIASES__: ['-h'], __ACTIVE__: True}
		self.opt_hash[__VERSION__] = { __ALIASES__: ['--version'], __ACTIVE__: True}

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
	# 		(WORK IN PROGRESS)	'prefix': --logging true
	#							'field'	: --file=/some/data
	#
	def add_suboptions(self, master, data):
		if master not in self.opt_hash: self.opt_hash[master] = {}
		for key, value in data.iteritems():
			if value[1] == __PREFIX__: warnings.warn("Not implemented yet") ; return
			if key not in self.opt_hash[master]: self.opt_hash[master][key] = {}
			self.opt_hash[master][key][__ALIASES__] = [key]
			self.opt_hash[master][key][__TYPE__] = value[1]
			self.opt_hash[master][key][__DATAFIELD__] = value[0]
			self.opt_hash[master][key][__NOTE__] = value[2]

	# Create aliases for a master command that invoke the same
	# functions as the actual master command.
	# 
	# This can be used to shorten commands that user need to
	# input (such as 'rails server' vs 'rails s' does it)
	#
	def set_master_aliases(self, master, aliases):
		if master not in self.opt_hash: warnings.warn("Could not identify master command. Aborting!") ; return
		if master not in aliases: aliases.append(master)
		self.opt_hash[master][__ALIASES__] = aliases

	# Allow a master command to bind to a sub field.
	def set_master_fields(self, master, fields):
		self.opt_hash[master][__BINDING__] = fields

	# Define a failsafe function to handle failed parsing attempts
	# If no function was registered default logging to STOUT will be used
	#
	def register_failsafe(self, funct):
		self.failsafe_function = funct

	# Defines the helper handles that are used to print the help screen.
	#
	def define_help_handle(self, helpers):
		self.opt_hash[__HELPER__][__ALIASES__] = helpers

	# Enable the helper handle (and list it in the helper screen)
	#
	def set_help_handle(self, boolean):
		self.opt_hash[__HELPER__][__ACTIVE__] = boolean

	# Defines the version handles that are used to print the version number of .
	#
	def define_version_handle(self, versions):
		self.opt_hash[__VERSION__][__ALIASES__] = versions

	# Enable the version handle (and list it in the helper screen)
	#
	def set_version_handle(self, boolean):
		self.opt_hash[__VERSION__][__ACTIVE__] = boolean

	# Set a version string to be printed in the help screen and/or version handle
	def set_container_version(self, version):
		self.container_version = version

	# Define fields for a command that gets handled above sub commands.
	# Slave fields should be a hash with a string key and tuple value attached
	# to it. A one tuple can also be replaced with the actual information.
	# So:
	# 'field' => ('information', "Description of the field")
	# and
	# 'field' => 'information'
	# are both valid field types.
	#
	def define_fields(self, fields):
		if self.slave_fields == None: self.slave_fields = {}
		for key, value in fields.iteritems():
			if key not in self.slave_fields: self.slave_fields[key] = {}
			self.slave_fields[key] = value

	# Key is the name of a field.
	# Value is a tuple of information to be passed down to a callback function when the field is
	# triggered.
	# A one tuple can also be replaced with the actual information
	#
	# So:
	# 'key' => ('information', "Description of the field")
	# and
	# 'key' => 'information'
	# are both valid field types.
	#
	def add_field(self, key, value):
		if self.slave_fields == None: self.slave_fields = {}
		self.slave_fields[key] = value

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
			self.opt_hash[master][key][__ALIASES__] = value + list(set(self.opt_hash[master][key][__ALIASES__]) - set(value))

	# Enables debug mode on the parser.
	# Will for example output the parsed and translated/ chopped strings to the console.
	#
	def enable_debug(self):
		self.debug = True

	# Print tree of options hashes and bound slave fields to master commands
	#
	def print_tree(self):
		if self.debug: print "[DEBUG]:", self.opt_hash

	# Parse a string either from a method parameter or from a commandline
	# argument. Calls master command functions with apropriate data attached
	# to it.
	#
	def parse(self, c = None):
		for alias in self.opt_hash[__HELPER__][__ALIASES__]:
			if c == alias:
				self.help_screen()
				return
		
		for alias in self.opt_hash[__VERSION__][__ALIASES__]:
			if c == alias:
				print self.container_version
				return

		content = (sys.args if (c == None) else c.split())
		counter = 0
		master_indices = []
		focus = None

		for item in content:
			for master in self.opt_hash:
				if "__" not in master:
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
					# print sub_counter
					if sub_counter == 0:
						focus = self.__alias_to_master(cmd)
						# print focus, cmd
						if focus in self.opt_hash:
							if self.opt_hash[focus][__BINDING__]:
								wait_for_slave = True
								sub_counter += 1
								continue

					else:
						rgged = cmd.replace('=', '= ').split()

						for sub_command in rgged:
							# print "Sub command:", sub_command
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
									if sub_command in self.slave_fields:
										slave_field = (sub_command, self.slave_fields[sub_command])
									else:
										if self.failsafe_function == None:
											print "An Error occured while parsing arguments."
										else:
											self.failsafe_function(cmd, 'Unknown Arguments')
										return
									continue

								trans_sub_cmd = self.__alias_to_sub(focus, sub_command)

								if trans_sub_cmd == None:
									if sub_command in self.opt_hash:
										if self.opt_hash[sub_command][__BINDING__]:
											# if self.debug: print "Waiting for slave field..."
											wait_for_slave = True
											continue

								if trans_sub_cmd in self.opt_hash[focus]:
									data_transmit[trans_sub_cmd] = True
									if trans_sub_cmd not in subs: subs.append(trans_sub_cmd)

					sub_counter += 1
				self.opt_hash[focus][__FUNCT__](focus, slave_field, subs, data_transmit)
				return
			counter += 1
		if self.failsafe_function == None:
			print "Error! No arguments recognised."
		else:
			self.failsafe_function(content, 'Invalid Options')

		# Return false if nothing was handled for container application to be able to
		raise Warning

	# Generates a help screen for the container appliction.
	#
	def help_screen(self):
		_s_ = " "
		_ds_ = "   "
		_dds_ = "      "
		# print "%-5s" % "Usage: Poke [Options]"

		# if self.debug: print "[DEBUG]: Your terminal's width is: %d" % width
		if not self.container_name and self.debug: print "[DEBUG]: Container application name unknown!" ; self.container_name = "default"


		if not self.opt_hash: print "Usage:", self.container_name
		else: print "Usage:", self.container_name, "[options]"

		print ""
		
		if self.opt_hash: print _s_ + "General:"
		if self.opt_hash[__VERSION__][__ACTIVE__]:
			print _ds_ + "%-20s %s" % (self.__clean_aliases(self.opt_hash[__VERSION__][__ALIASES__]), "Print the version of"), "'%s'" % self.container_name
		
		if self.opt_hash[__HELPER__][__ACTIVE__]:
			print _ds_ + "%-20s %s" % (self.__clean_aliases(self.opt_hash[__HELPER__][__ALIASES__]), "Print this help screen")

		print ""

		if self.opt_hash: print _s_ + "Commands:"
		for key, value in self.opt_hash.iteritems():
			if "__" not in key:
				print _ds_ + "%-20s %s" % (self.__clean_aliases(value[__ALIASES__]), value[__NOTE__])
				for k, v in self.opt_hash[key].iteritems():
					if "__" not in k:
						print _dds_ + "%-22s %s" % (self.__clean_aliases(v[__ALIASES__]), v[__NOTE__])

		print ""

		if self.slave_fields: print _s_ + self.fields_name + ":"
		for key, value in self.slave_fields.iteritems():
			description = str(value)[1:-1].replace("\'", "")
			print _ds_ + "%-20s %s" % (key, description)

	def __clean_aliases(self, aliases):
		string = ""
		counter = 0
		for alias in aliases:
			counter += 1
			string += alias
			if counter < len(aliases): string += ", "
		return string

	def __alias_to_master(self, alias):
		for key, value in self.opt_hash.iteritems():
			if "__" not in key:
				for map_alias in value[__ALIASES__]:
					if alias == map_alias:
						return key
		return None

	def __alias_to_sub(self, master, alias):
		for key, value in self.opt_hash[master].iteritems():
			if "__" not in key:
				if alias in value[__ALIASES__]:
					return key
		return None