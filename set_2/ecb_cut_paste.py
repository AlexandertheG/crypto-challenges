#!/usr/bin/python

import sys
import binascii
import base64
from Crypto.Cipher import AES

#Solutuion: python ecb_cut_paste.py decrypt 5530b16ebe34d6f8eda91450982c0ba30561813961791fb4b24985e81ba6307a70f8252c96b04b46f5c80e31371fa5cc8b48e6d89b57fdef89841c234b305dfe
#5530b16ebe34d6f8eda91450982c0ba30561813961791fb4b24985e81ba6307a - email=ab@aaaacd.com&uid=10&role=
#70f8252c96b04b46f5c80e31371fa5cc8b48e6d89b57fdef89841c234b305dfe - admin&uid=10&role=user

def parse_params(param_str):
	
	my_dict = {}
	params = param_str.split('&')
	for i in params:
		j = i.split('=')
		if not my_dict.has_key(j[0]):
			my_dict[j[0]] = j[1]

	return my_dict

def profile_for(prfl):

	if '&' in prfl or '=' in prfl:
		raise "Invalid characters not allowed"
	
	my_dict = {}
	enc_prfl = ''
	my_dict['email'] = prfl
	enc_prfl+='email' + '=' + prfl +'&'
	my_dict['uid'] = str(10)
	enc_prfl+='uid' + '=' + my_dict['uid'] +'&'
	my_dict['role'] = 'user'
	enc_prfl+='role' + '=' + 'user'
	
	return enc_prfl

def aes_ecb_encrypt(msg, key):

	msg = pad_msg(msg, len(key))
        aes = AES.new(key, AES.MODE_ECB)
        res = aes.encrypt(msg)

        return res

def aes_ecb_decrypt(msg, key):

        aes = AES.new(key, AES.MODE_ECB)
        decr_msg = aes.decrypt(msg)
	#decr_msg = remove_padding(decr_msg)
	
	return decr_msg

def pad_msg(msg, key_length):

        padding_length = key_length - len(msg)%key_length
        for i in range(0, padding_length):
                msg+=chr(padding_length)

        return msg

def remove_padding(msg):
	pad_lng = ord(msg[len(msg)-1])
	return msg[0:len(msg)-pad_lng]
	

key = "rrtUHftKcXZlpRTr"
if sys.argv[1] == "encrypt":
	profile = sys.argv[2]
	encoded_prfl = profile_for(profile)
	encrypted_prfl = aes_ecb_encrypt(encoded_prfl, key)
	print encrypted_prfl.encode('hex')
elif sys.argv[1] == "decrypt":
	encr_str = sys.argv[2].decode('hex')
	decrypted_prfl = aes_ecb_decrypt(encr_str, key)
	print decrypted_prfl
	print parse_params(decrypted_prfl)
