#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os, fnmatch, re

def find(pattern, path):
	result = []
	for root, dirs, files in os.walk(path):
		for name in files:
			if fnmatch.fnmatch(name,pattern):
				result.append(os.path.join(root, name))
		return result

f = open('./article_list.txt', 'r')
list = f.read().decode('ascii','ignore').encode('utf-8').splitlines()
pres_list = list
list = [re.sub('[(.*)]','',title) for title in list]
list = [re.sub('[-]',' ',title) for title in list]
list = [title.replace(' ',',') for title in list]
list = [title.split(',') for title in list]
list = [[item for item in title if item != ''] for title in list]

doc_num = 0
doc_list = []
for i in range(len(list)):
	result = []
	if len(list[i]) >= 3:
		result = find('*' + list[i][0] + '*' + list[i][1] + '*' + list[i][2] + '*.txt', '/Users/dcmitchell/Desktop/LMP/TXT')
		if len(result) == 0:
			result = find('*' + list[i][0] + '*' + list[i][1] + '*.txt', '/Users/dcmitchell/Desktop/LMP/TXT')
			if len(result) == 0:
				result = find('*' + list[i][0] + '*.txt', '/Users/dcmitchell/Desktop/LMP/TXT')

	elif len(list[i]) == 2:
		result = find('*' + list[i][0] + '*' + list[i][1] + '*.txt', '/Users/dcmitchell/Desktop/LMP/TXT')
		if len(result) == 0:
			result = find('*' + list[i][0] + '*.txt', '/Users/dcmitchell/Desktop/LMP/TXT')

	elif len(list[i]) == 1:
		result = find('*' + list[i][0] + '*.txt', '/Users/dcmitchell/Desktop/LMP/TXT')

	if len(result) < 4 and len(result) > 0:
		
		f2r = open(result[0],"r")
		entry = f2r.read()
		entry = re.sub(r'.*Your article','',entry,0,re.DOTALL)
		entry = re.sub(r'.*OPTIONAL\]','',entry,0,re.DOTALL)

		f2r.close()

		f2w = open('./DocsByID/' + str(doc_num) + ".txt","a")
		f2w.write(entry)
		f2w.close() 

		doc_list.append([doc_num,pres_list[i]])
		doc_num += 1
		print doc_num-1, list[i], pres_list[i], result

f = open('./DocsByID/DocKey',"a")
for i in doc_list:
	f.write(str(i[0]) + " : " + i[1] + '\n')

f.close()
