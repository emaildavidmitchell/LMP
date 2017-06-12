#!/usr/bin/env python3

import re, os, nltk, string, pprint
from unidecode import unidecode

class Classifier():
	
	def __init__(self,key_path):
		self.key = self.get_key(key_path)
		self.word_features = self.get_corpus()
		self.training_set = self.train_classifier()
		self.classifier = self.build_classifier()

	def get_key(self,key_path):
		f = open(key_path,'r')
		key = f.readlines()
		key = [entry.split(":") for entry in key]
		for i in key:
			if len(i) != 3:
				print(i)
				print(len(i))
		key = [[d.strip(),a.strip(),c.strip()] for (d,a,c) in key]
		return key

	def get_corpus(self):
		words = []
		for (d,a,c) in self.key:
			tokens = nltk.word_tokenize(self.remove_punc(a))
			for word in tokens:
				words.append(word)
		words = set(words)
		return words

	def document_features(self,document):
		document_words = set(nltk.word_tokenize(self.remove_punc(document)))
		features = {}
		for word in self.word_features:
			features['contains({})'.format(word)] = word in document_words
		
		punctuation = [",","(",")","'","`","-","."]
		for p in punctuation:
			features['contains({})'.format(p)] = p in document

		contains_english = False
		for word in document_words:
			if self.is_english(word) == True:
				contains_english = True
		features['contains_english'] = contains_english

		features['contains_digits'] = self.is_number(document_words)

		features['contains_names'] = self.contains_name(document_words)

		features['is_one_word'] = len(document_words) == 1

		features['is_two_words'] = len(document_words) == 2

		features['is_greater_than_two_words'] = len(document_words) > 2

		features['contains_ism'] = "ism" in document

		features['contains_, The'] = ", The" in document

		return features

	def is_number(self,words):
		engl_numbers = ['one','two','three','four','five','six','seven','eight','nine','eleven','twelve','thirteen','fourteen','fifteen','sixteen', 'seventeen','eighteen','nineteen','ten','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety','thousand','million','billion','trillion','quadrillion']
		for word in words:
			if word.lower() in engl_numbers:
				print("true")
				return True
			for c in word:
				if c.isdigit():
					print("true")
					return True
		return False

	def is_english(self,word):
		if not nltk.corpus.wordnet.synsets(word.lower()):
			return False
		else: 
			return True

	def contains_name(self,words):
		names = nltk.corpus.names.words()
		for word in words:
			if word in names:
				return True
		return False

	def build_classifier(self):
		classifier = nltk.NaiveBayesClassifier.train(self.training_set)
		return classifier

	def classify(self,a):
		a = self.document_features(a)
		return self.classifier.classify(a)

	def train_classifier(self):
		documents = []
		for (d,a,c) in self.key:
			if c.lower() in ('p','w','m','o'):
				documents.append([self.document_features(a),c])
		return documents

	def remove_punc(self,line):
		line = line.translate(line.maketrans('', '', string.punctuation))
		return line

cl = Classifier('./DocsByID/DocKey')
cl.classifier.show_most_informative_features(10)
for (d,a,c) in cl.key:
	print(a," is a ",cl.classify(a))