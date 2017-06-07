#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import sys
import numpy

class Tagger():
	def __init__(self,filename):
		self._text = open(filename,"r+").read().decode('ascii', 'ignore').encode('utf-8')
		self._text = self._text.replace('\n',' ')
		self._classified_text = []
		self.tag()

	def tag(self):
		tokenizer = nltk.data.load('nltk:tokenizers/punkt/english.pickle')
		tokenized = tokenizer.tokenize(self._text)
		try:
			for i in tokenized:
				words = nltk.word_tokenize(i)
				tagged = nltk.pos_tag(words)
				namedEnt = nltk.ne_chunk(tagged, binary=True)
				self._classified_text.append(namedEnt)

		except Exception as e:
			print(str(e))
			pass


tagger = Tagger("./Abbey Theatre.txt")
#tagger._classified_text[10].draw()
for i in tagger._classified_text:
	print(i)
