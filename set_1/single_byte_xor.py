#!/usr/bin/python
import sys
import collections
import string

cypher_lst = list(sys.argv[1])
freq_percent = collections.defaultdict(int)
byte_lst = []
result = "foo"
freq_score = 0
keywords=['the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up', 'out', 'if', 'about', 'who', 'get', 'which', 'go', 'me', 'when', 'make', 'can', 'like', 'time', 'no', 'just', 'him', 'know', 'take', 'people', 'into', 'year', 'your', 'good', 'some', 'could', 'them', 'see', 'other', 'than', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'new', 'want', 'because', 'any', 'these', 'give', 'day', 'most', 'us']

def look_up(tmp_str):

	global result
	global freq_score

	list_str = tmp_str.lower().split(' ')

	max_score = 0

	for i in list_str:
		if i in keywords:
			max_score+=1
	
	if max_score > freq_score:
		freq_score = max_score
		result = tmp_str

i = 0 

while i < len(cypher_lst):
	byte_hex = ''
	byte_hex+=cypher_lst[i]
	i+=1
	byte_hex+=cypher_lst[i]
	i+=1
	
	byte_lst.append(byte_hex)

for i in range(65, 123):
	tmp_result = ''
	for el in range(0, len(byte_lst)):
		tmp_result+=chr(i^int(str(byte_lst[el]), base=16))
	
	look_up(tmp_result)

print result
