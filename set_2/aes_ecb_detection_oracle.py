#!/usr/bin/python

import sys
import random
import binascii
import base64
from Crypto.Cipher import AES

def generate_rand_bytes(lgth):

	rand_bytes = ''
	for i in range(0,lgth):
		rand_bytes+=chr(random.randint(0, 255))
	
	return rand_bytes

def get_rand_num(start, end):

	return random.randint(start, end)

def aes_ecb_encrypt(byte_array, key):

        aes = AES.new(key, AES.MODE_ECB)
	res = aes.encrypt(byte_array)
        
	return res

def aes_cbc_encrypt(msg, key, iv):
        encr_res = ''
        num_of_blocks = len(msg)/len(key)
        for block_num in range(0, num_of_blocks):
                iv = aes_ecb_encrypt(xor_bytes(msg[block_num*len(key):block_num*len(key)+len(key)], iv), key)
                encr_res+=iv
	
        return encr_res

def pad_msg(msg, key_length):
        padding_length = key_length - len(msg)%key_length

	if padding_length != key_length:
	        for i in range(0, padding_length):
        	        msg+=chr(padding_length)

        return msg

def xor_bytes(byte_arr1, byte_arr2):
        xored_arr = ''
        for b in range(0, len(byte_arr1)):
                xored_arr+=chr(ord(byte_arr1[b])^ord(byte_arr2[b]))

        return xored_arr

def encryption_oracle(plain_txt):

	rand_lgth_begin = get_rand_num(4, 10)
	rand_lgth_end = get_rand_num(4, 10)
	
	key = generate_rand_bytes(16)
	res_plain_txt = pad_msg(generate_rand_bytes(rand_lgth_begin) + plain_txt + generate_rand_bytes(rand_lgth_end), len(key))
	
	iv = generate_rand_bytes(16)
	pick_algo = get_rand_num(0, 2)

	if pick_algo == 1:
		print "==="+"ecb"+"==="
		ascii_res = aes_ecb_encrypt(res_plain_txt, key)
		detect_mode(ascii_res, len(key))
	else:
		print "==="+"cbc"+"==="
		ascii_res = aes_cbc_encrypt(res_plain_txt, key, iv)
		detect_mode(ascii_res, len(key))

def detect_mode(cipher_txt, block_size):
	
	ecb_count = 0
	num_of_blocks = len(cipher_txt)/block_size
	for bt in range(0, block_size):
		for num in range(2, num_of_blocks):
			if cipher_txt[block_size+bt] == cipher_txt[block_size*num+bt]:
				ecb_count+=1

	if ecb_count-1 == (num_of_blocks-2) or ecb_count-1 > (num_of_blocks-2):
		print "Detected ECB"
	else:
		print "Detected CBC"

text_in = sys.argv[1]
encryption_oracle(text_in)
