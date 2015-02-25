# =========================================================
# Copyright: (c) 2015 Katharina Sabel
# License  : LGPL 3.0 (See LICENSE)
# Comment  : Testing script for options parser
#
# =========================================================

# Prepare application path
import sys
sys.path.append('../src/')

import adv_opt_parse as parser

def connect(master, fields, sub, data):
	print master, fields, sub, data

p = parser.OptParseAdv({'connect':(connect, "Connect to servers"), 'copy':(connect, "Copy files to a server")})
p.set_container_name("Poke")
# p.enable_debug()
p.print_tree()

# p.set_master_fields('connect', True)
p.set_master_aliases('connect', ['c'])
p.set_master_aliases('copy', ['cp'])
# p.define_fields({'nas':'192.168.2.131'})
p.add_suboptions('connect', {'-X': (None, parser.__VALUE__, "Enable X forwarding for the current session (if not enabled by default)"), '--cmd': (None, parser.__FIELD__, "Push a command to a remote server")})
p.sub_aliases('connect', {'-X': ['-X'], '--cmd': ['-c']})

p.help_screen()

# poke connect serverA

# p.parse('c nas -X')

#########################
#   TEST SCRIPT BELOW   #
#########################


# [Master Command] [ Slave Field (if not None) ] [ List of Sub Commands ] [ Sub command data hash ]
# 
#
# def connect(master, fields, subs, data):
# 	print master, fields, subs, data

# def copy(master, fields, subs, data):
# 	pass #print master, "This is a copy with", sub, "and", data

# p = OptParseAdv({'connect':connect})
# # p.enable_debug()

# p.set_master_fields('connect', True)
# p.master_aliases('connect', ['c'])

# p.define_fields({'nas':'192.168.2.131'})

# p.add_suboptions('connect', {'-X': (None, __VALUE__), '--command': (None, __FIELD__)})
# # p.add_suboptions('copy', {'--file': (None, __FIELD__)})
# p.sub_aliases('connect', {'-X': ['-X'], '--command': ['-c']})
# # p.sub_aliases('copy', {'--file': ['-f']})


# # p.print_debug()

# p.parse('c nas -X')



# [spacekookie@Alarei Poke]$ poke
# Usage: poke [options]

# Options:
#   --version     show program's version number and exit
#   -?            Open preferred editor to edit your config files!

#   Overwrite Settings:
#     -K SSH_KEY  Overwrite stored key-setting for a server. Note: this is
#                 usually not very useful. Add the apropriate key to your
#                 keys.cfg file instead!
#     -X          Overwrite XTerm settings for the ssh session

#   Your servers:
#     -j, --jane  Connect to Jane's NAS:[Jane@111.222.333.444] with key
#                 'default'. XTerm is 'False' by default
#     -w, --work  Connect to Work Cluster:[employee1337@workserver.kiwi] with
#                 key 'work'. XTerm is 'True' by default

# Other commands:
#   purge			Deletes Poke from your system
#   upgrade		Checks if there are new stable releases of Poke
#   upgrade-unstable	Also includes unstable releases in upgrade search