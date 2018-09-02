#!/usr/bin/python
import sys
import base64

plain_txt = sys.argv[1]
pad_to = int(sys.argv[2])

padding_length = pad_to - len(plain_txt)

if padding_length > 0:
	hex_length = hex(padding_length)[2:]
	if len(hex_length) == 1:
		hex_length = str(0) + str(hex(padding_length)[2:])

	pad_hex = "\\x" + hex_length

	for i in range(0, padding_length):
		plain_txt+=pad_hex

print plain_txt
