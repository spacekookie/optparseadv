#!/usr/bin/python

import re

text = 'add -f -X --name="some cool shit" --path=/path/here'

# Magic RegEx
pattern = "([a-zA-Z0-9]+ (((((--([a-zA-Z0-9]+ )(([a-zA-Z0-9]+=[a-zA-Z0-1]+ )*))+))|(([a-zA-Z0-9]+=[a-zA-Z0-1]+ )+)|)))*"
#pattern = "([a-zA-Z-_]+[A-Z]*)=*(\"([\w\W]*)\"|/([\w\W]+))*"

# ([a-z]*-*_*[A-Z]*)=*("([\w\W]*)"|/([\w\W]*))*

# rgged = re.split(mega, text)

# print rgged

output = re.split(pattern, text)

print output, "\n"

output2 = [x for x in output if x != None and x != ' ' and x != '' and '"' not in x]

print output2

print ['add-server', '-f', '-X', '--name', 'some cool shit', '--path', '/path/here']

# input1 = '--note="This is some note"'

# input2 = input1
# # del input[2]

# output = re.search("\W", input1).group(1)

# # = re.search(, input2)

# # output = re.split(, input2)
# # input1.split('"')

# print output