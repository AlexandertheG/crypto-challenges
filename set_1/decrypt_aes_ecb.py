import base64
from Crypto.Cipher import AES

def read_in():
	return open("base64.txt").read().rstrip()

def aes_ecb_decrypt(byte_array):
	aes = AES.new("YELLOW SUBMARINE", AES.MODE_ECB)
	return aes.decrypt(byte_array)

base64_str = read_in()
byte_arr = str(base64.b64decode(base64_str))
plaintext = aes_ecb_decrypt(byte_arr)
print plaintext
