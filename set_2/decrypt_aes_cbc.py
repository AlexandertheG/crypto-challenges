import base64
import random
import binascii
from Crypto.Cipher import AES

def read_in():
        return open("base64.txt").read().rstrip()

def aes_ecb_encrypt(byte_array, key):

	aes = AES.new(key, AES.MODE_ECB)
	return aes.encrypt(byte_array)

def aes_ecb_decrypt(byte_array, key):

	aes = AES.new(key, AES.MODE_ECB)
        return aes.decrypt(byte_array)

def aes_cbc_encrypt(msg, key, iv):
	encr_res = ''
	num_of_blocks = len(msg)/len(key)
	for block_num in range(0, num_of_blocks):
		iv = aes_ecb_encrypt(xor_bytes(msg[block_num*len(key):block_num*len(key)+len(key)], iv), key)
		encr_res+=iv
	
	return base64.b64encode(encr_res)

def aes_cbc_decrypt(msg, key, cipher_block):
        decr_res = ''
	msg = base64.b64decode(msg)
	num_of_blocks = len(msg)/len(key)
	for block_num in range(0, num_of_blocks):
		tmp_cipher = msg[block_num*len(key):block_num*len(key)+len(key)]
                decr_res += xor_bytes(aes_ecb_decrypt(msg[block_num*len(key):block_num*len(key)+len(key)], key), cipher_block)
                cipher_block = tmp_cipher

        return decr_res

def xor_bytes(byte_arr1, byte_arr2):
	xored_arr = ''
	for b in range(0, len(byte_arr1)):
		xored_arr+=chr(ord(byte_arr1[b])^ord(byte_arr2[b]))
	
	return xored_arr

def pad_msg(msg, key_length):
	padding_length = key_length - len(msg)%key_length

	if padding_length != key_length:
	        for i in range(0, padding_length):
        	        msg+=chr(padding_length)
	
	return msg

def test_cbc():
	msg  = "Lorem Ipsum is simply dummy text of the printing and typesetting industry"
	key = "YELLOW SUBMARINE"
	iv_dec = [random.randrange(0, 256) for i in range(0, len(key))]
	iv = ''
	for i in range(0, len(iv_dec)):
		iv+=chr(iv_dec[i])

	msg = pad_msg(msg, len(key))
	encr_msg = aes_cbc_encrypt(msg, key, iv)
	msg_plain = aes_cbc_decrypt(encr_msg, key, iv)
	print msg_plain

#test_cbc()
key = "YELLOW SUBMARINE"
iv = ''
for i in range(0, len(key)):
	iv+=key[i]
cipher_msg = read_in()
msg_plain = aes_cbc_decrypt(cipher_msg, key, iv)
print msg_plain
