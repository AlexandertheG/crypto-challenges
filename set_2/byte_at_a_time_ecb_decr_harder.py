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

def generate_rand_prefix(lgth):

	lgth = random.randint(0, lgth)
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

def pad_msg(msg, key_length):
        padding_length = key_length - len(msg)%key_length
        for i in range(0, padding_length):
                msg+=chr(padding_length)

        return msg

def encryption_oracle(plain_txt):
	
	res_plain_txt = pad_msg(plain_txt + base64.b64decode(base64_fl), len(key))
	
	return aes_ecb_encrypt(res_plain_txt, key)

def generate_dict(blk):
	dict_res = {}

	encr = encryption_oracle(blk + chr(10))
        dict_res[encr[0:len(blk)+1]] = chr(10)
	for j in range(32, 127):
		encr = encryption_oracle(blk + chr(j))
		dict_res[encr[0:len(blk)+1]] = chr(j)

	return dict_res

def detect_block_size(cipher_txt):

	block_sizes = [32, 24, 16]
	blk_sz = 0
	for i in range(0, 16):
		for sz in block_sizes:
			if cipher_txt[i:i+sz] in cipher_txt[i+sz:]:
				blk_sz = sz

	return blk_sz

def decrypt_unknown_string(lookup, blk, msg_lng):
	
	unknown_res = ''
	for i in range(0, msg_lng):
		ecb_res = encryption_oracle(blk[0:len(blk)-i])
		if ecb_res[0:len(blk)+1] in lookup:
			c = lookup[ecb_res[0:len(blk)+1]]
			unknown_res+=c

		blk = blk[0:len(blk)-i-1]+unknown_res
		lookup = generate_dict(blk)
		
	return unknown_res

key="lhjlHKhLJhgOHyoh"
base64_fl = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
text_in = sys.argv[1]
text_in += generate_rand_prefix(100)
ascii_aes_encr = encryption_oracle(text_in)
blk_sz = detect_block_size(ascii_aes_encr)

decr_str = base64.b64decode(base64_fl)
msg_lng = len(decr_str)
padded_lng = msg_lng + (blk_sz-msg_lng%blk_sz)
blk = ''
for c in range(0, padded_lng-1):
	blk+='A'

lookup_dict = generate_dict(blk)
res = decrypt_unknown_string(lookup_dict, blk, msg_lng)

print res
