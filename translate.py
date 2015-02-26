# -*- coding: utf-8 -*-

from naive_bayes import NaiveBayesSBLM
from copy import deepcopy

class Translator:

	def __init__(self):
		self.dictionary = dict()
		self.sentences = list()
		self.translation = dict()
                self.spanish_pos_dict = dict()
		self.pos_dict = dict()
		self.sentence_count = 0
		#TODO: create custom func to parse corpus
		corpusPath = 'data/wiki_corpus.txt'
		trainingCorpus = self.read_corpus(corpusPath)
		self.naive_bayes = NaiveBayesSBLM(trainingCorpus)

  
	def read_corpus(self, filename):
		try:
			f = open(filename).read()
		except:
			return []
		f = f.replace(',', '')
		f = f.replace('\'', '')
		f = f.replace('\"', '')
		f = f.replace('!', '')
		f = f.replace('?', '')
		f = f.replace('(', '')
		f = f.replace(')', '')
		f = f.replace('[', '')
		f = f.replace(']', '')
		f = f.replace('$', '')
		f = f.replace('#', '')
		f = f.replace('@', '')
		f = f.replace('%', '')
		f = f.replace('*', '')
		f = f.lower()
		# remove other chars as necessary
		corpus = f.split('.')
		for i in range(len(corpus)):
			corpus[i] = corpus[i].split()	
		return corpus

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
			words.append(self.get_word(op).strip())
		return words

	# finds the English translation that matches the part of speech of the Spanish word, if there is one
	def choose_matching_pos(self, options, token):
		spanish_pos = token[1]
		english_pos = self.pos_dict[spanish_pos]
		matching_options = list()
		if english_pos != 'None':
			for op in options:
				if len(op) > 0: # there will be no options for whitespace or punctuation
					if self.get_pos(op) == english_pos:
						matching_options.append(self.get_word(op).strip())
				else:
					matching_options.append(op)
		if len(matching_options) > 0:
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
		final_options = self.choose_matching_pos(options, key)
		return final_options


	# eliminate cases of duplicate words and make each word its own token for NaiveBayes
	def dedup_and_separate(self, sentence):
		uniquified = list()
		for token in sentence:
			split = token.split() # separate out words
			for elem in split:
				if len(uniquified) == 0:
					uniquified.append(elem)
				elif uniquified[-1] != elem: # don't append duplicate elements
					uniquified.append(elem)
		return uniquified

	# compares all possible sentences to find the most probable
	def get_best(self, sentences):
		best_sent = list()
		best_score = float('-inf')
		for sent in sentences:
			updated = self.dedup_and_separate(sent)
			score = self.naive_bayes.score(updated)
			if score > best_score:
				best_sent = deepcopy(sent)
				best_score = score
		return best_sent

	# creates ans stores all permutations of the translation words from the bilingual dictionary
	def generate_sentences(self, sent_ops):
		all_sents = list()
		if len(sent_ops) > 0:
			for op in sent_ops[0]:
				seed_list = [op]
				all_sents.append(seed_list)
			for i in range(1, len(sent_ops)):
				temp_list = list()
				for option in sent_ops[i]:
					new_list = deepcopy(all_sents)
					for sent in new_list:
						sent.append(option)
						temp_list.append(sent)
				all_sents = deepcopy(temp_list)

		return all_sents


	# choose best english sentence from a list of list of possible words
	def choose_best_sentence(self, sent_ops):
		if len(sent_ops) <= 0:
			return []
		sentences = self.generate_sentences(sent_ops)
		best = self.get_best(sentences)
		print "BEST: " + str(best)
		return best


	# basic direct translation
	def stupid_translate(self):
		for line in self.sentences:
			english_sentence = list()
			self.sentence_count += 1

			for word in line:
				poss_words = self.translate(word)
				english_sentence.append(poss_words) # list of lists of potential translations at each index

			best_sentence = self.choose_best_sentence(english_sentence) # use Naive Bayes to get the most likely sentence
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


if __name__ == '__main__':
	main()
