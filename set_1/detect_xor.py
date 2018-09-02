#!/usr/bin/python
import sys
import collections
import string

freq_percent = collections.defaultdict(int)
keywords=['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us']


def decrypt(byte_lst, key):
	tmp_result = ''
        for el in range(0, len(byte_lst)):
        	tmp_result+=chr(key^int(str(byte_lst[el]), 16))

        return tmp_result


def read_in():
	
	global freq_score
	global result
	for ln in open("xor_file.txt"):
		
		line = ln.rstrip()
		i = 0
		byte_list = []

		while i < len(line):
			byte_hex = ''
			byte_hex+=line[i]
			i+=1
			byte_hex+=line[i]
			i+=1
	
			byte_list.append(byte_hex)
		
		for i in range(0, 255):
			max_score = 0
			tmp_result = decrypt(byte_list, i)

			list_str = tmp_result.lower().split(' ')
		
			for word in list_str:
                		if word in keywords:
					max_score+=1	
					#print tmp_result
					#break

			if max_score > freq_score:
				freq_score = max_score
				result = tmp_result

result = "foo"
freq_score = 0
read_in()
print result
