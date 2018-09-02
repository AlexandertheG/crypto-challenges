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

def pad_msg(msg, key_length):
        padding_length = key_length - len(msg)%key_length
        for i in range(0, padding_length):
               	msg+=chr(padding_length)

        return msg

def aes_cbc_encrypt(msg, key, iv):
        encr_res = ''
        num_of_blocks = len(msg)/len(key)
        for block_num in range(0, num_of_blocks):
                iv = aes_ecb_encrypt(xor_bytes(msg[block_num*len(key):block_num*len(key)+len(key)], iv), key)
                encr_res+=iv

        return encr_res

def aes_cbc_decrypt(msg, cipher_block):
	global is_pad_val
	is_pad_val = False
        decr_res = ''
        msg = base64.b64decode(msg)
        num_of_blocks = len(msg)/len(key)
        for block_num in range(0, num_of_blocks):
                tmp_cipher = msg[block_num*len(key):block_num*len(key)+len(key)]
                decr_res += xor_bytes(aes_ecb_decrypt(msg[block_num*len(key):block_num*len(key)+len(key)], key), cipher_block)
                cipher_block = tmp_cipher
	
	is_pad_val = padding_valid(decr_res, len(key))

        return decr_res

def aes_ecb_encrypt(byte_array, key):

        aes = AES.new(key, AES.MODE_ECB)
        res = aes.encrypt(byte_array)

        return res

def aes_ecb_decrypt(byte_array, key):

        aes = AES.new(key, AES.MODE_ECB)
        return aes.decrypt(byte_array)

def xor_bytes(byte_arr1, byte_arr2):
        xored_arr = ''
        for b in range(0, len(byte_arr1)):
                xored_arr+=chr(ord(byte_arr1[b])^ord(byte_arr2[b]))

        return xored_arr

def padding_valid(in_str, key_lngth):

        pad_lngth = ord(in_str[len(in_str) - 1])
        valid_pad = True

	if pad_lngth == 0 or pad_lngth > 16:
		return False

        for i in range(0, pad_lngth):
                if ord(in_str[len(in_str) - pad_lngth + i]) != pad_lngth:
                        valid_pad = False
                        break
        return valid_pad


def cbc_attack(cphr_str, iv):

	num_blk = len(cphr_str)/16
	cphr_blks = []
	res = ''

	for i in range(0, num_blk):
		cphr_blks.append(cphr_str[i*16:i*16+16])

	for i in range(0, num_blk):
		int_cphr = []
		tmp_res = ''
		for j in range(0, len(iv)):
			tmp_ascii = ord(iv[len(iv) - 1 - j])
			for k in range(0, 256):
				xor_chr = chr(k^(j + 1))
				tmp_list = list(iv)
				tmp_list[len(iv)-1-j] = xor_chr
				iv = ''
				for m in tmp_list:
					iv+=m
				decr = aes_cbc_decrypt(base64.b64encode(cphr_blks[i]), iv)
				if is_pad_val == True and ord(decr[len(decr) - 1]) == j + 1:
					int_cphr.append(k)
					tmp_count = 0
					for p in range((len(iv) - 1 - j), len(iv)):
						tmp_list[len(iv) - 1 - tmp_count] = chr(int_cphr[len(iv) - (len(iv) - tmp_count)]^(j+1+1))
						tmp_count+=1

					iv = ''
	                                for m in tmp_list:
        	                                iv+=m
		
					tmp_res+=chr(tmp_ascii^k)
					break

		for r in range(0, len(tmp_res)):
			res+=tmp_res[len(tmp_res) - 1 - r]

		iv = cphr_blks[i]

	print res

#key ="ETohYlKjgYhsdmcV"
#iv = "HJladhfslHOIhsdB"
is_pad_val = False
key = generate_rand_bytes(16)
iv = generate_rand_bytes(16)
str_lst = ["MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=",
"MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=",
"MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==",
"MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==",
"MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl",
"MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==",
"MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==",
"MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=",
"MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=",
"MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"]

rand_str = str_lst[random.randint(0, 9)]
ascii_str = base64.b64decode(rand_str)
padded_msg = pad_msg(ascii_str, 16)
cphr = aes_cbc_encrypt(padded_msg, key, iv)
#print "C - b64: " + base64.b64encode(cphr)
#print "C - b16: " + binascii.hexlify(cphr)
#print "IV - b64: " + base64.b64encode(iv)
#print "IV - b16: " + binascii.hexlify(iv)
#decr_msg = aes_cbc_decrypt(base64.b64encode(cphr), iv)
cbc_attack(cphr, iv)
#print padding_valid(decr_msg, len(key))
#print ord(decr_msg[len(decr_msg) - 1])
