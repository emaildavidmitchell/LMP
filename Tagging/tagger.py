#!/usr/bin/env python
# -*- coding: utf-8 -*-

from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import sys

class Tagger():
	def __init__(self,filename):
		self._text = open(filename,"r+").read().decode('ascii', 'ignore').encode('utf-8')
		self._classified_text = []
		self.tag()

	def tag(self):
		st = StanfordNERTagger('/Users/dcmitchell/Desktop/LMP/stanford-ner/classifiers/english.muc.7class.distsim.crf.ser.gz',
					   '/Users/dcmitchell/Desktop/LMP/stanford-ner/stanford-ner.jar',
					   encoding='utf-8')
		tokenized_text = word_tokenize(self._text)
		self._classified_text = st.tag(tokenized_text)

tagger = Tagger(sys.argv[1])
for i in tagger._classified_text:
	print(i)