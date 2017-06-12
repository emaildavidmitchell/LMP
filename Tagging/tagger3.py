#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk, re, pprint
from nltk.corpus import conll2000



class POSTagger():
	def __init__(self,filename):
		self.text = open(filename,"r+").read().decode('ascii', 'ignore').encode('utf-8')
		self.text = self.text.replace('\n', ' ')
		self.tagged_text = []
		self.tag()

	def tag(self):
		tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
		sentences = tokenizer.tokenize(self.text)
		sentences = [nltk.word_tokenize(sent) for sent in sentences]
		sentences = [nltk.pos_tag(sent) for sent in sentences]
		self.tagged_text = sentences

train_sents = conll2000.chunked_sents('train.txt', chunk_types=['NP'])
pos_tagger = POSTagger("./Abbey Theatre.txt")


for i in pos_tagger.tagged_text:
	print (nltk.ne_chunk(i))







