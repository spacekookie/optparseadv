"""
Test script - State reader machine
===========
Reads sentences according to states.

:copyright: (C) 2015 Katharina Sabel <SpaceKookie>
:license: GPLv2 (See LICENSE)
"""

_A_ = 'A'
_B_ = 'B'
_C_ = 'C'

class StateReader():

	def __init__(self, input_lang):
		input_lang += " "
		STATE = _A_

		collection = []
		current = ""
		index = 0

		for char in input_lang:
			index += 1
			# print "Char", char
			# print "State:", STATE
			# print "Current:", current
			# print ""


			if STATE == _A_:
				
				if self.non_empty(char):
					current += char
					STATE = _B_

				elif char == " ":
					STATE = _A_

				else:
					# Handle the error here!
					print "ERROR 1"			

			elif STATE == _B_:
				if self.non_empty(char):
					current += char
					STATE = _B_

				elif self.quote(char):
					current += char
					STATE = _C_

				elif char == " ":
					collection.append(current)
					current = ""
					STATE = _A_

				else:
					# Handle the error here!
					print "ERROR 2"

			elif STATE == _C_:
				if not self.quote(char):
					current += char
					STATE = _C_
				else:
					current += char
					collection.append(current)
					current = ""
					STATE = _A_

			else:
				print "ERROR 3"

		print collection
		print index

	def non_empty(self, char):
		if char != " " and char != '"' and char != "'": return True
		return False 

	def quote(self, char):
		if char == "'" or char == '"': return True
		return False

string = 'add-server --note="This is some note" path=~/Documents/cat.txt -f'

sr = StateReader(string)
