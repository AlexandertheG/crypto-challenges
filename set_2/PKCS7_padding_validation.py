import sys
import binascii

def padding_valid(in_str):

	pad_lngth = int(binascii.hexlify(in_str[len(in_str)-1]), base=16)
	valid_pad = True
	for i in range(0, pad_lngth):
		if int(binascii.hexlify(in_str[len(in_str) - pad_lngth + i]), base=16) != pad_lngth:
			valid_pad = False
			break
	return valid_pad

str_invalid = b'ICE ICE BABY\x01\x02\x03\x04' #b'ICE ICE BABY\x04\x04\x04\x05'
str_valid = b'ICE ICE BABY\x04\x04\x04\x04'

is_valid = padding_valid(str_invalid)
print is_valid
is_valid = padding_valid(str_valid)
print is_valid
