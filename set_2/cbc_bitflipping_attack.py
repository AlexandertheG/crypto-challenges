#!/usr/bin/python

import sys
import random
import binascii
import base64
from Crypto.Cipher import AES

def sanitize_input(in_str):
	build_str = ''
	for i in range(0, len(in_str)):
		if in_str[i] == ";" or in_str[i] == "=":
			build_str = build_str
		else:
			build_str+=in_str[i]

	return build_str

def pad_msg(msg, key_length):
	global msg_is_padded
        padding_length = key_length - len(msg)%key_length
	
	if padding_length > 0:
		msg_is_padded = True
        	for i in range(0, padding_length):
                	msg+=chr(padding_length)

        return msg

def aes_cbc_encrypt(msg, key, iv):
        encr_res = ''
        num_of_blocks = len(msg)/len(key)
        for block_num in range(0, num_of_blocks):
                iv = aes_ecb_encrypt(xor_bytes(msg[block_num*len(key):block_num*len(key)+len(key)], iv), key)
                encr_res+=iv

        return base64.b64encode(encr_res)

def xor_bytes(byte_arr1, byte_arr2):
        xored_arr = ''
        for b in range(0, len(byte_arr1)):
                xored_arr+=chr(ord(byte_arr1[b])^ord(byte_arr2[b]))

        return xored_arr

def aes_ecb_encrypt(byte_array, key):

        aes = AES.new(key, AES.MODE_ECB)
        return aes.encrypt(byte_array)

def aes_ecb_decrypt(byte_array, key):

        aes = AES.new(key, AES.MODE_ECB)
        return aes.decrypt(byte_array)

def aes_cbc_decrypt(msg, key, cipher_block):
        decr_res = ''
        msg = base64.b64decode(msg)
        num_of_blocks = len(msg)/len(key)
        for block_num in range(0, num_of_blocks):
                tmp_cipher = msg[block_num*len(key):block_num*len(key)+len(key)]
                decr_res += xor_bytes(aes_ecb_decrypt(msg[block_num*len(key):block_num*len(key)+len(key)], key), cipher_block)
                cipher_block = tmp_cipher

	if msg_is_padded == True:
		decr_res = remove_padding(decr_res)
	
	return decr_res

def split_string_by_char(str, by_char):
	
	return str.split(by_char)
	
def remove_padding(padded_msg):
	padded_msg = bytes(padded_msg)
        pad_lngth = int(binascii.hexlify(padded_msg[len(padded_msg)-1]), base=16)
	
	return padded_msg[0:len(padded_msg) - pad_lngth]

def flip_bits(msg):
	byte_msg = bytes(base64.b64decode(msg))
	flp_byte1 = ord(byte_msg[21])^0x01
	flp_byte2 = ord(byte_msg[27])^0x01
	flp_msg = ''

	for i in range(0, len(byte_msg)):
		if i == 21:
			flp_msg+=chr(flp_byte1)
		elif i == 27:
			flp_msg+=chr(flp_byte2)
		else:
			flp_msg+=byte_msg[i]

	return base64.b64encode(flp_msg)

usr_input = sys.argv[1]
prepend_str = "comment1=cooking%20MCs;userdata="
append_str = ";comment2=%20like%20a%20pound%20of%20bacon"
key = "lhjlHKhLJhgOHyoh"
iv = "XakUhKeGGHbswRMl"
msg_is_padded = False
sanitized_usr_input = prepend_str + sanitize_input(usr_input) + append_str
padded_str = pad_msg(sanitized_usr_input, len(key))
base64_cbc_str = aes_cbc_encrypt(padded_str, key, iv)
base64_cbc_str = flip_bits(base64_cbc_str)
cbc_decr = aes_cbc_decrypt(base64_cbc_str, key, iv)
tuples = split_string_by_char(cbc_decr, ";")
if "admin=true" in tuples:
	print cbc_decr
