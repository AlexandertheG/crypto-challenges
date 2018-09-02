#!/usr/bin/python

#usage: repeating_XOR.py <file_name> <key>

import sys
import base64


def process_line(ln):

	str_lst = ln
	global i
	global xored_str
	xored_str = ''
	j = 0
	while j < len(str_lst):
		tmp_byte = hex((ord(str_lst[j])^ord(key[i%3])))[2:]
		if len(tmp_byte) == 1:
			tmp_byte = "0" + tmp_byte
		xored_str+=tmp_byte
		i+=1
		j+=1


key = list(sys.argv[2])
f_name = sys.argv[1]
fh = open(f_name, "r")
xored_str = ''
i = 0
ln_num = 0
for ln in fh:
	#routine to process new-line char
	if ln_num > 0:
		bt = hex((ord('\n')^ord(key[i%3])))[2:]
		xored_str+=bt
		print xored_str
		i+=1	
	line = ln.rstrip()
	process_line(line)
	ln_num+=1

print xored_str
			
