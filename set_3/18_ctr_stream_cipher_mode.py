#!/usr/bin/python
import base64
from Crypto.Cipher import AES
import Crypto.Util.Counter

def aes_ecb_encrypt(byte_array):

        aes = AES.new(key, AES.MODE_ECB)
        return aes.encrypt(byte_array)

def xor_bytes(byte_arr1, byte_arr2):
        xored_arr = ''
        for b in range(0, len(byte_arr1)):
                xored_arr+=chr(ord(byte_arr1[b])^ord(byte_arr2[b]))

        return xored_arr

def encr_ctr(num):
	num+=1
	hex_num = hex(num)[2:].zfill(16)[::-1]
	return hex_num

def ctr_decrypt(ciphertext):
	ctr = -1
	deciphr = ""

	num_blks = len(ciphertext)/blk_sz
	if len(ciphertext)%blk_sz != 0:
        	num_blks+=1

	for i in range(0, num_blks-1):
		#tmp = encr_ctr(ctr).decode("hex")
        	inter_encr_blk = aes_ecb_encrypt(nonce.decode("hex") + chr((ctr+1)%256) + "00000000000000".decode("hex"))
	        deciphr+=xor_bytes(inter_encr_blk, ciphertext[i*blk_sz:i*blk_sz+blk_sz])
        	ctr+=1

	#decrypt the remaining bytes
	tmp = encr_ctr(ctr).decode("hex")
	inter_encr_blk = aes_ecb_encrypt(nonce.decode("hex") + chr((ctr+1)%256) + "00000000000000".decode("hex"))

	remain_lngth = 0
	if len(ciphertext)%blk_sz != 0:
        	remain_lngth = len(ciphertext)%blk_sz
	else:
        	remain_lngth = blk_sz

	deciphr+=xor_bytes(inter_encr_blk[0:remain_lngth], ciphertext[(num_blks-1)*blk_sz:(num_blks-1)*blk_sz + remain_lngth])
	
	return deciphr

def ctr_encrypt(plain):
	return ctr_decrypt(plain)

blk_sz = AES.block_size
cph_txt = base64.b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")
plain_txt = "Lorem Ipsum is simply dummy text of the printing and typesetting industry"
key = "YELLOW SUBMARINE"
nonce= "0000000000000000"

print ctr_decrypt(cph_txt)
#print ctr_encrypt(plain_txt)
