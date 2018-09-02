#!/usr/bin/python
import base64
from Crypto.Cipher import AES
import Crypto.Util.Counter

def aes_ecb_encrypt(byte_array):

        aes = AES.new(key, AES.MODE_ECB)
        return aes.encrypt(byte_array)

####################################
def xor_bytes(byte_arr1, byte_arr2):
        xored_arr = ''
        for b in range(0, len(byte_arr1)):
                xored_arr+=chr(ord(byte_arr1[b])^ord(byte_arr2[b]))

        return xored_arr

########################
def encr_ctr(num):
        num+=1
        hex_num = hex(num)[2:].zfill(16)[::-1]
        return hex_num

#########################
def ctr_decrypt(ciphertext):
        ctr = -1
        deciphr = ""

        num_blks = len(ciphertext)/blk_sz
        if len(ciphertext)%blk_sz != 0:
                num_blks+=1

        for i in range(0, num_blks-1):
                inter_encr_blk = aes_ecb_encrypt(nonce.decode("hex") + "0000000000000000".decode("hex"))
                deciphr+=xor_bytes(inter_encr_blk, ciphertext[i*blk_sz:i*blk_sz+blk_sz])
                ctr+=1

        #decrypt the remaining bytes
        tmp = encr_ctr(ctr).decode("hex")
        inter_encr_blk = aes_ecb_encrypt(nonce.decode("hex") +  "0000000000000000".decode("hex"))

        remain_lngth = 0
        if len(ciphertext)%blk_sz != 0:
                remain_lngth = len(ciphertext)%blk_sz
        else:
                remain_lngth = blk_sz

        deciphr+=xor_bytes(inter_encr_blk[0:remain_lngth], ciphertext[(num_blks-1)*blk_sz:(num_blks-1)*blk_sz + remain_lngth])

        return deciphr

#############################
def ctr_encrypt(plain):
        return ctr_decrypt(plain)

#################################
def crack_xor(encr_txt, crck_key):
	xored_arr = ''
	key_byte_pos = 0
        for b in range(0, len(encr_txt)):
                xored_arr+=chr(ord(encr_txt[b])^ord(crck_key[key_byte_pos]))
		key_byte_pos += 1

		if key_byte_pos == 16:
			key_byte_pos = 0
		
        return xored_arr


key = "YELLOW SUBMARINE"
nonce= "0000000000000000"
blk_sz = AES.block_size

fl = open('base_64.txt', 'r')

test_txt = "AAAAAAAAAAAAAAAA"
encr = ctr_encrypt(test_txt)
guess_key = xor_bytes(test_txt, encr)

for ln in fl:
	decoded_64 = base64.b64decode(ln.strip())
	encr = ctr_encrypt(decoded_64)
	print crack_xor(encr, guess_key)
