# -*- coding: utf-8 -*-

class Translator:

	def __init__(self):
		self.dictionary = dict()
		self.sentences = list()
		self.translation = dict()
		self.sentence_count = 0

	# function to remove complex characters and punctuation
	def simplify(self, word):
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
		return word


	# starter function to look up a word (later make more complicated/intelligent)
	def translate(self, word):
		key = self.simplify(word)
		options = self.dictionary[key]
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
	def parse_dict(self, dictionary):
		f = open(dictionary)
		for line in f:
			split = line.split(':')
			if len(split) == 2:
				key = split[0] # spanish word
				values = split[1].split(',') # multiple possible english words for a single spanish word
				self.dictionary[key] = values
			else:
				print split # if anything prints, there's a problem with the dictionary
		f.close() # clean up after yourself!

def main():
	sentences_file = 'data/sentences.txt'
	dictionary_file = 'data/dictionary.txt'
	t = Translator()
	t.parse_dict(dictionary_file)
	t.read_file(sentences_file)
	t.stupid_translate()

	print t.translation

if __name__ == '__main__':
	main()