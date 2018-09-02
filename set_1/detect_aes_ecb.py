import base64

def read_in():
	return open("base64.txt").readlines()

def detect_aes_ecb(hex_lines):
	block_count_dict = {}
	for ln in hex_lines:
		line = ln.rstrip()
		num_of_blocks = len(line)/2/key_length
		for blk_num in range(0, num_of_blocks-1):
			same_blocks = 0
			repeat_blk = ''
			for blk_num2 in range(blk_num+1, num_of_blocks):
				s1 = line[blk_num*key_length*2:blk_num*key_length*2+32]
				s2 = line[blk_num2*key_length*2:blk_num2*key_length*2+32]
				if s1 == s2:
					same_blocks+=1
					repeat_blk = line[blk_num*key_length*2:blk_num*key_length*2+32]
		
			if same_blocks > 0 and repeat_blk not in block_count_dict:
				block_count_dict[repeat_blk] = same_blocks
	
	for k,v in block_count_dict.iteritems():
		print "Block " + k + " repeated this # of times: " + str(v+1)

key_length = 16
hex_txt = read_in()
detect_aes_ecb(hex_txt)
