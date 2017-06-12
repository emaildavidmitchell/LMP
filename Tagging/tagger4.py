#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk, re, pprint, wikipedia
from nltk.corpus import conll2000
from nltk.tokenize import word_tokenize


class BigramChunker(nltk.ChunkParserI):
	def __init__(self, train_sents):
		train_data = [[(t,c) for w,t,c in nltk.chunk.tree2conlltags(sent)] for sent in train_sents]
		self.tagger = nltk.BigramTagger(train_data)

	def parse(self, sentence):
		pos_tags = [pos for (word,pos) in sentence]
		tagged_pos_tags = self.tagger.tag(pos_tags)
		chunktags = [chunktag for (pos,chunktag) in tagged_pos_tags]
		conlltags = [(word, pos, chunktag) for ((word,pos),chunktag) in zip(sentence, chunktags)]
		return conlltags
		#return nltk.chunk.conlltags2tree(conlltags)


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
bigram_chunker = BigramChunker(train_sents)
pos_tagger = POSTagger("./Abbey Theatre.txt")

chunked_doc = [bigram_chunker.parse(sent) for sent in pos_tagger.tagged_text]
#chunked_doc = [nltk.chunk.tree2conlltags(sent) for sent in pos_tagger.tagged_text]

nes = []
for sent in chunked_doc:
	phrase = []
	for i in range(len(sent)):
		w,t,c = sent[i]
		if len(phrase) == 0 and c == "B-NP":
			phrase.append(w)
		elif len(phrase) > 0 and c == "B-NP":
			nes.append(phrase)
			phrase = [w]
		elif len(phrase) > 0 and c == "I-NP":
			phrase.append(w)
		elif len(phrase) == 0 and c == "I-NP":
			phrase.append(w)
		elif len(phrase) > 0:
			nes.append(phrase)
			phrase = []

		if (i == len(sent)-1) and len(phrase) > 0:
			nes.append(phrase)



nes = [' '.join(np) for np in nes]
for i in nes:
	print i, "Wiki entry: ", wikipedia.search(i)






