#!/usr/bin/python

import sys

arg1 = list(sys.argv[1])
arg2 = list(sys.argv[2])

result_str = ''

for i in range(0, len(arg1)):
	result_str+=str(int(arg1[i], base=16)^int(arg2[i], base=16))

print result_str
