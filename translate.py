# -*- coding: utf-8 -*-

from naive_bayes import NaiveBayesSBLM
from holbrook_corpus import HolbrookCorpus

class Translator:

	def __init__(self):
		self.dictionary = dict()
		self.sentences = list()
		self.translation = dict()
                self.spanish_pos_dict = dict()
		self.pos_dict = dict()
		self.sentence_count = 0
		#TODO: create custom func to parse corpus
		trainPath = 'data/holbrook-tagged-train.dat'
		trainingCorpus = TrainingCorpus(trainPath)
		self.naive_bayes = NaiveBayesSBLM(trainingCorpus)
		

	# function to remove complex characters and punctuation
	def simplify(self, word_pos):
		tokens = word_pos.split('(')
                tokens[1] = tokens[1].replace(')', '')
		word = tokens[0]
		word = word.strip()
		word = word.lower()
		word = word.replace('á', 'a')
		word = word.replace('í', 'i')
		word = word.replace('é', 'e')
		word = word.replace('ó', 'o')
		word = word.replace('ú', 'u')
		word = word.replace('ñ', 'n')
		word = word.replace('.', '')
		word = word.replace(',', '')
		tokens[0] = word
		return tokens

	# gets the tagged part of speech from a word-POS pair, separated by '/'
	def get_pos(self, pair):
		tokens = pair.split('/')
		return tokens[1]

	# gets the word from a word-POS pair, separated by '/'
	def get_word(self, pair):
		tokens = pair.split('/')
		return tokens[0]

	# takes a list of options and returns a list of just the words
	def options_to_words(self, options):
		words = list()
		for op in options:
			list.append(self.get_word(op).strip())
		return words

	# finds the English translation that matches the part of speech of the Spanish word, if there is one
	def choose_matching_pos(self, options, token):
		pos = token[1]
		english_pos = self.pos_dict[pos]
		matching_options = list()
		if english_pos != None:
			for op in options:
				if self.get_pos(op) == english_pos:
					matching_options.append(self.get_word(op).strip())
		if len(matching_option) > 0:
			return matching_options
		else:
			# none of the options match the part of speech, so just return all of them
			return self.options_to_words(options)

	# starter function to look up a word (later make more complicated/intelligent)
	def translate(self, word):
		key = self.simplify(word)
		if key[0] != ',' and key[0] != '.' and len(key[0]) > 0: # ignore punction
			options = self.dictionary[key[0]]
		else:
			options = [key[0]] # punctuation needs no translation
		options = self.choose_matching_pos(options, key)
		return options
		#NOTE: need to strip() all possible words

	#NOTE: sent is a list() of list()
	#		curr_sent is a list() of str
	#		best_sent is a tuple of list() of str and float
	def best_sent_helper(self, sent_ops, curr_sentence, best_sent, best_score):
		curr_sent = curr_sentence
		if len(curr_sent) > len(sent_ops): 	#catchall case
			return [best_sent, best_score]
		if len(curr_sent) == len(sent_ops):
			score = self.naive_bayes.score(curr_sent)
			if score > best_score:
				return [curr_sent, score]
			else:
				return [best_sent, best_score]

		options = sent_ops[len(curr_sent)]
		for word in options:
			curr_sent[len(curr_sent)] = word
			best = self.best_sent_helper(sent_ops, curr_sent, best_sent, best_score)
			best_sent = best[0]
			best_score = best[1]
		return [best_sent, best_score]


	# choose best english sentence from a list of list of possible words
	# NOTE: At some point, will need to handle rearrangement of words in sentence.
	# 		That should be done before this step.
	def choose_best_sent(self, sent_ops):
		if len(sent_ops) <= 0:
			return []
		curr_sentence = list()
		best_sent = list()
		best_score = 0.0
		best = self.best_sent_helper(sent_ops, curr_sentence, best_sent, best_score)
		return best


	# basic direct translation
	def stupid_translate(self):
		for line in self.sentences:
			english_sentence = list()
			self.sentence_count += 1

			for word in line:
				poss_words = self.translate(word)
				english_sentence.append(poss_words)

			best_sentence = self.choose_best_sent(english_sentence)
			self.translation[self.sentence_count] = best_sentence


	# read in a file and convert into usable form
	def read_file(self, file_name):
		contents = list()
		f = open(file_name)
		for line in f:
			contents.append(line)
		f.close() # clean up after yourself!

		for line in contents:
			words = line.split()
			sentence = list()
			for word in words:
				sentence.append(word)
			self.sentences.append(sentence)

		return contents

	# reads in our mini dictionary and makes usable
	def parse_dict(self, filename):
		dictionary = dict() 
		f = open(filename)
		for line in f:
			split = line.split(':')
			if len(split) == 2:
				key = split[0] # spanish word
				values = split[1].split(',') # multiple possible english words for a single spanish word
				dictionary[key] = values
			else:
				print "ERROR" # if anything prints, there's a problem with the dictionary
		f.close() # clean up after yourself!
		return dictionary

        # reads in the Spanish POS to English POS dictionary, works like "parse_dict"
        def parse_pos_dict(self, filename):
                dictionary = dict()
                f = open(filename)
                for line in f:
                        split = line.split(': ')
                        if len(split) == 2:
                                key = split[0]
                                value = split[1].rstrip()
                                if value == "None":
                                        dictionary[key] = None
                                else:
                                        dictionary[key] = value
                        else:
                                print "ERROR"
                f.close()
                return dictionary

def main():
	sentences_file = 'data/tagged_sentences.txt'
	dictionary_file = 'data/output_dictionary.txt'
	pos_file = 'data/type_conversions.txt'
	t = Translator()
	t.pos_dict = t.parse_pos_dict(pos_file)
	t.dictionary = t.parse_dict(dictionary_file)
	t.read_file(sentences_file)
	t.stupid_translate()

        print t.translation

if __name__ == '__main__':
	main()
