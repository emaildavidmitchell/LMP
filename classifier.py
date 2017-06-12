#!/usr/bin/env python3

import re, os, nltk, string, pprint
from unidecode import unidecode

class Classifier():

	def __init__(self,key=None):
		self.key = key
		self.word_features = []
		self.training_set = []
		self.classifier = ''

	def anglocize(self,word):
		word = unidecode(word)
		return word

	def get_words(self,directory,filename,line_limit=None):
		words = []
		path = directory + filename
		f = open(path).readlines()
		for line in f[:line_limit]:
			line = line.translate(line.maketrans('', '', string.punctuation))
			line = nltk.word_tokenize(line)
			for word in line:
				words.append(self.anglocize(word.lower()))
		return words		
		
	def get_words_with_article_name(self,directory,filename,line_limit=3):
		words = []
		path = directory + filename
		article_name = self.key[filename]
		article_name = self.prep_article_name(article_name)
		f = open(path).readlines()
		for line in f[:line_limit]:
			if self.does_line_contain(line,article_name):
				line = line.translate(line.maketrans('', '', string.punctuation))
				line = nltk.word_tokenize(line)
				for word in line:
					words.append(self.anglocize(word.lower()))
		return words		
		
	def does_line_contain(self,line,article_name):
		for word in article_name:
			if word in line:
				return True
		return False

	def get_corpus(self,directory):
		words = []
		for filename in os.listdir(directory):
			if filename.endswith("0.txt"):
				print("Building corpus from %s" % filename)
				for word in self.get_words(directory,filename):
					words.append(word) 
		words = nltk.FreqDist(words).most_common(2000)
		self.word_features = [w for w,c in words]

	def document_features(self,document,article_name):
		document_words = set(document)
		features = {}
		for word in self.word_features:
			features['contains({})'.format(word)] = word in document_words
		features['name_comma'] = "," in article_name
		return features

	def get_training_set(self,directory,categories):
		documents = []
		for cat in categories:
			print("Getting training set for %s" % cat)
			directory2 = directory+"/"+cat+"/"
			for filename in os.listdir(directory2):
				if filename.endswith(".txt"):
					documents.append([self.get_words(directory2,filename),cat])
		self.training_set = [(self.document_features(d), c) for (d,c) in documents]


	def build_classifier(self):
		classifier = nltk.NaiveBayesClassifier.train(self.training_set)
		self.classifier = classifier

	def classify_file(self,directory,filename):
		document = self.get_words(directory,filename)
		features = self.document_features(document,self.key)
		return self.classifier.classify(features)

	def classify_dir(self,directory):
		classification = []
		for filename in os.listdir(directory):
			if filename.endswith("0.txt"):
				print("Classifiying %s" % filename)
				classification.append([self.key[filename],self.classify_file(directory,filename)])

		return classification
	
	def prep_article_name(self,article_name):
		article_name = self.anglocize(article_name)
		article_name = article_name.split(",")
		article_name = list(reversed(article_name))
		article_name = [word.translate(word.maketrans('', '', string.punctuation)) for word in article_name]
		return article_name
	
f = open("./DocsByID/DocKey")
f = f.readlines()
f = [entry.split(":") for entry in f]
key = {}
for entry in f:
	key[entry[0].strip() + ".txt"] = entry[1].strip()


nbc = Classifier(key)
nbc.get_corpus("./DocsByID/")
nbc.get_training_set("./training",["organization","person","work"])
nbc.build_classifier()
classification = nbc.classify_dir("./DocsByID/")
for i in classification:
	print(i)
nbc.classifier.show_most_informative_features(100)



