# -*- coding: utf-8 -*-

class Translator:

	def __init__(self):
		self.dictionary = dict()
		self.sentences = list()
		self.translation = dict()
		self.pos_dict = dict()
		self.sentence_count = 0

	# function to remove complex characters and punctuation
	def simplify(self, word_pos):
		tokens = word_pos.split('(')
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

	# finds the English translation that matches the part of speech of the Spanish word, if there is one
	def choose_best(self, options, token):
		word = token[0]
		pos = token[1]
		english_pos = self.pos_dict[pos]
		if english_pos is not None:
			for op in options:
				if self.get_pos(op) == english_pos:
					return self.get_word(op)
		return self.get_word(options[0]) # none of the options match the part of speech, so just return the first one

	# starter function to look up a word (later make more complicated/intelligent)
	def translate(self, word):
		print word
		key = self.simplify(word)
		if key[0] != ',' and key[0] != '.' and len(key[0]) > 0: # ignore punction
			options = self.dictionary[key[0]]
		else:
			options = [key[0]] # punctuation needs no translation
		option = self.choose_best(options, key)
		return options[0] # this can be modified later to not just use the first translation option

	# basic direct translation
	def stupid_translate(self):
		for line in self.sentences:
			english_sentence = list()
			self.sentence_count += 1

			for word in line:
				english_word = self.translate(word)
				english_word = english_word.strip()
				english_sentence.append(english_word)

			self.translation[self.sentence_count] = english_sentence




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
				print split # if anything prints, there's a problem with the dictionary
		f.close() # clean up after yourself!
		return dictionary

def main():
	sentences_file = 'data/tagged_sentences.txt'
	dictionary_file = 'data/output_dictionary.txt'
	pos_file = 'data/type_conversions.txt'
	t = Translator()
	t.pos_dict = t.parse_dict(pos_file)
	t.dictionary = t.parse_dict(dictionary_file)
	t.read_file(sentences_file)
	t.stupid_translate()

	print t.translation

if __name__ == '__main__':
	main()