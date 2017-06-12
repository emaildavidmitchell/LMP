#!/usr/bin/env python3

import re, os, nltk, string, pprint
from unidecode import unidecode

class Classifier():
	
	def __init__(self,key_path,training_path):
		self.key = self.get_key(key_path)
		self.training_set = self.train_classifier(training_path)
		self.classifier = self.build_classifier()

	def get_key(self,key_path):
		f = open(key_path,'r')
		key = f.readlines()
		key = [entry.split(":") for entry in key]
		key = [[d.strip(),a.strip(),c.strip()] for (d,a,c) in key]
		return key

	def document_features(self,document):
		document_words = set(nltk.word_tokenize(self.remove_punc(document.lower())))
		features = {}
		features['contains_born'] = "born" in document.lower()
		features['contains_was_born_in'] = "was born in" in document.lower()
		features['contains_b.'] = "b." in document.lower()
		features['contains_month'] = self.contains_month(document_words)
		features['short_sentence'] = len(document_words) < 5
		features['contains_name'] = self.contains_name(document_words)
		features['contains_year_range'] = self.contains_range(document)
		features['contains_decade'] = self.contains_decade(document)

		return features

	def contains_month(self,words):
		months = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december"]
		for word in words:
			if word.lower() in months:
				return True
		return False

	def contains_decade(self,sent):
		sent = sent.replace(" ","")
		if re.search('[0-9]{4}.[s]',sent) != None:
			return True
		return False

	def contains_range(self,sent):
		sent = sent.replace(" ","")
		if re.search('[0-9]{4}[-][0-9]*',sent) != None:
			return True
		return False

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

	def train_classifier(self,training_path):
		tset= []
		docs = self.open_and_get_sentences(training_path+"birthday_neg.txt")
		for sent in docs:
			tset.append([self.document_features(sent),"neg"])

		docs = self.open_and_get_sentences(training_path+"birthday_pos.txt")
		for sent in docs:
			tset.append([self.document_features(sent),"pos"])
		
		return tset

	def open_and_get_sentences(self,path):
		sents = []
		f = open(path,"r")
		sents = f.readlines()
		sents = [s.strip() for s in sents]
		f.close()

		return sents

	def remove_punc(self,line):
		line = line.translate(line.maketrans('', '', string.punctuation))
		return line

cl = Classifier('./DocsByID/DocKey','./training/birthday/')
cl.classifier.show_most_informative_features(10)
print(cl.classify("b. 1946"))