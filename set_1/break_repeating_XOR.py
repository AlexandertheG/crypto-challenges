#!/usr/bin/python

import binascii
import sys
import base64
import array

def read_in():

	global original_hex
	global original_hex_str
	for line in fh:
		line = line.rstrip('\n')
		line = binascii.hexlify(base64.b64decode(line))
		original_hex_str+=line
		
	for j in xrange(0, len(original_hex_str), 2):
		original_hex.append(original_hex_str[j:j+2])	


def find_edit_dist(hex_str1, hex_str2):
	
	list_str1 = []
	list_str2 = []

	for j in xrange(0, len(hex_str1), 2):
		list_str1.append(hex_str1[j:j+2])
		list_str2.append(hex_str2[j:j+2])	
	

	dist = 0

	for i in range(0, len(list_str1)):
		bin1 = list(bin(int(list_str1[i], 16))[2:].zfill(8))
		bin2 = list(bin(int(list_str2[i], 16))[2:].zfill(8))
		
		for l in range(0, len(bin1)):
			if bin1[l] != bin2[l]:
				dist+=1

	return dist

def find_keysize():
	global min_edit_dist
	global min_key_size
	for l in range(2, 41):
		total_dist = 0.00
		num_blocks = len(original_hex)/l - 1
		for k in range(0, num_blocks):
			total_dist += float(find_edit_dist(original_hex_str[k*2*l:k*2*l + 2*l], original_hex_str[k*2*l + 2*l:k*2*l + 2*l + 2*l])/l)
		
		avg_dist = float(total_dist/num_blocks)
		if avg_dist < min_edit_dist:
			min_edit_dist = avg_dist
			min_key_size = l

	transpose_blocks()

def transpose_blocks():
	global transposed_hex
	global transposed_block_length
	transposed_block_length = len(original_hex)/min_key_size
	if len(original_hex)%min_key_size != 0:
		transposed_block_length+=1
	
	padding = 0
	if len(original_hex)%min_key_size != 0:
		padding = min_key_size - len(original_hex)%min_key_size	
	
	tmp_original_hex = list(original_hex)
	for n in range(0, padding):
		tmp_original_hex.append("00")

	pos = 0
	for i in range(0, min_key_size):
		count = i
		for j in range(0, len(tmp_original_hex)/min_key_size):
			hex_byte = tmp_original_hex[count]
			transposed_hex[pos] = hex_byte
			count+=min_key_size
			pos+=1

def init_ascii():
	global ascii_dec_list
	for i in range(0, 256):
		ascii_dec_list.append(i)

def one_byte_xor():
	num_of_trans_blocks = len(transposed_hex)/transposed_block_length
	global key_bytes
	for b in range(0, num_of_trans_blocks):
		histogram_max = 0
		tmp_char = 'init'
		solved_block = ''
		for ascii_char in range(0, len(ascii_dec_list)):
			histogram_str = ''
			for cipher_byte in range(0, transposed_block_length):
				dec = ascii_dec_list[ascii_char]^int(str(transposed_hex[b*transposed_block_length + cipher_byte]), 16)
				if (dec > 47 and dec < 58) or (dec > 96 and dec < 123) or (dec > 64 and dec < 91) or dec == 32 or dec == 45 or dec == 47 or dec == 92 or dec == 10 or dec== 44 or dec == 46 or dec == 63:
					histogram_str+=chr(dec)
			
			if len(histogram_str) > histogram_max:
				histogram_max = len(histogram_str)
				tmp_char = chr(ascii_dec_list[ascii_char])
		
		key_bytes+=tmp_char

def decrypt_cipher():
	plain_text = ''
	for i in range(0, len(original_hex)):
		plain_text+=chr(ord(key_bytes[i%min_key_size])^int(str(original_hex[i]), 16))
	
	print plain_text

min_edit_dist = 99999.99
min_key_size = 999
transposed_block_length = 0
f_name = sys.argv[1]
fh = open(f_name, "r")
ascii_dec_list = []
init_ascii()
#hex_file = open("hex_file.txt", "w")
original_hex = []
original_hex_str = ''
transposed_hex = {}
read_in()
find_keysize()
key_bytes = ''
one_byte_xor()
decrypt_cipher()
