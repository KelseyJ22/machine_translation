# -*- coding: utf-8 -*-

from naive_bayes import NaiveBayesSBLM
from copy import deepcopy
import re

class Translator:

	def __init__(self):
		self.dictionary = dict()
		self.sentences = list()
		self.translation = dict()
		self.spanish_pos_dict = dict()
		self.pos_dict = dict()
		self.sentence_count = 0
		#TODO: create custom func to parse corpus
		corpusPath = 'corpora/wiki_tagless.txt'
		trainingCorpus = self.read_corpus(corpusPath)
		#self.naive_bayes = NaiveBayesSBLM(trainingCorpus)
		self.naive_bayes = NaiveBayesSBLM(trainingCorpus)
		self.vowels = set(['a','e','i','o','u'])

  
	def read_corpus(self, filename):
		try:
			f = open(filename).read()
		except:
			return []
		f = f.replace(',', '')
		f = f.replace('\'', '')
		f = f.replace('\"', '')
		f = f.replace('!', '.')
		f = f.replace('?', '.')
		f = f.replace('(', '')
		f = f.replace(')', '')
		f = f.replace('[', '')
		f = f.replace(']', '')
		f = f.replace('$', '')
		f = f.replace('#', '')
		f = f.replace('@', '')
		f = f.replace('%', '')
		f = f.replace('*', '')
		f = f.replace('-', '')
		f = f.replace('=', '')
		f = f.replace('[0-9]', '')
		f = f.lower()
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
		#word = word.replace('.', '')
		#word = word.replace(',', '')
		tokens[0] = word
		return tokens

	
    # find instances of reflexive verbs and replace "se" with an empty string to translate properly
	def replace_reflexive(self, word, next_word):
                word = self.simplify(word)
                next_word = self.simplify(next_word)
                if word[0] == 'se' and next_word[1].startswith('v'):
                        word[0] = ''
                        word[1] = 'None'
                return word


	# gets the tagged part of speech from a word-POS pair, separated by '/'
	def get_pos(self, pair):
		tokens = pair.split('/')
		if len(tokens) > 1:
			return tokens[1]
		else:
			return pair


	# gets the word from a word-POS pair, separated by '/'
	def get_word(self, pair):
		tokens = pair.split('/')
		if len(tokens) > 1:
			return tokens[0]
		else:
			return pair


	# finds the English translation that matches the part of speech of the Spanish word, if there is one
	def choose_matching_pos(self, options, token):
		spanish_pos = token[1]
		english_pos = self.pos_dict[spanish_pos]
		matching_options = list()
		if english_pos != 'None':
			for op in options:
				if len(op) > 0: # there will be no options for whitespace or punctuation
					if self.get_pos(op) == english_pos:
						matching_options.append(op)
				else:
					matching_options.append(op)
		if len(matching_options) > 0:
			return matching_options
		else:
			# none of the options match the part of speech, so just return all of them
			return options


	# starter function to look up a word (later make more complicated/intelligent)
	def translate(self, index, word, next_word):
		key = self.simplify(word)
                if key[0] == "como":
                        return self.handle_como(index, key[0])
                if next_word:
                        key = self.replace_reflexive(word, next_word)
		if key[0] != ',' and key[0] != '.' and len(key[0]) > 0: # ignore punctuation
			options = self.dictionary[key[0]]
		else:
			options = [key[0]] # punctuation needs no translation
		final_options = self.choose_matching_pos(options, key)
		return final_options



	# compares all possible sentences to find the most probable
	def get_best(self, sentences):
		best_sent = list()
		best_score = float('-inf')
		for sent in sentences:
			score = self.naive_bayes.score(sent)
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

                # Leaving the pos as part of the sentences also leaves in some pesky "\n" characters
                # so this loop removes them, but it also slows down the program and doesn't really
                # help. For debugging, it's nice, but when turning it in, we may want to remove this loop.
                for sent in all_sents:
                        for i, word in enumerate(sent):
                                sent[i] = word.replace("\n", "")
                                
                # There's probably a better way to do this, but it works for now.
                for i, sent in enumerate(all_sents):
                        new_sent = self.reorder_adjectives(sent)
                        if new_sent:
                                all_sents[i] = new_sent
                                new_new_sent = self.fix_negation(new_sent)
                                if new_new_sent:
                                        all_sents[i] = new_new_sent
                        else:
                                new_sent = self.fix_negation(sent)
                                if new_sent:
                                        all_sents[i] = new_sent
                                        

                return all_sents


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


	# fix word order to match typical English syntax
	def reorder_adjectives(self, sentence):
		result = sentence[:]
		for i, word in enumerate(sentence):
			if i == len(sentence) - 1:
				continue
			next_word = sentence[i+1]
			if word and next_word:  #making sure we don't have spaces or punctuation here
				if self.get_pos(word).startswith('NN') and self.get_pos(next_word).startswith('JJ'):
					result[i] = next_word
					result[i+1] = word
		return result


	# English negation is more complicated than Spanish, where you just precede the word with "no"
	def fix_negation(self, sentence):
		result = sentence[:]
		for i, word in enumerate(sentence):
			if i == len(sentence) - 1:
				continue
			next_word = sentence[i+1]
			if word and next_word:
				if self.get_word(word).strip() == 'no' and (self.get_pos(next_word).startswith('VB') or self.get_pos(next_word).startswith('IN')):
					verb = next_word.split(' ')
					verb[0] = "don't"
					fixed_verb = ' '.join(verb)
					result[i+1] = fixed_verb
					del result[i]
		return result


	# correct 'a' to 'an' if followed by a vowel
	def fix_a_an(self, sentence):
		result = sentence[:]
		for i, word in enumerate(sentence):
			if i == len(sentence) - 1:
				continue
			next_word = self.get_word(sentence[i+1])
			if word and next_word:
				if self.get_word(word).strip() is 'a':
					if next_word[0] in self.vowels:
						result[i] = 'an'
		return result


	# translate to "because" if como is at the beginning of the sentence
	def handle_como(self, index, word):
		options = self.dictionary[word]
		for op in options:
			if 'because' in self.get_word(op) and index == 1:
				return [op]
			elif index != 1 and 'WP' in self.get_pos(op):
				return [op]
			else:
				continue
			return options
        

    # instead of 'more _____' should be '________er'    
	def fix_adj(self, sentence):
		result = sentence[:]
		for i, word in enumerate(sentence):
			if i == len(sentence) - 1:
				continue
			next_word = sentence[i+1]
			if word and next_word:
				if self.get_word(word) == 'more':
					if self.get_pos(next_word) == 'JJ':
						result[i] = ''
						replacement = self.get_word(next_word) + 'er/' + self.get_pos(next_word)
						result[i+1] = replacement
		return result


	# takes a list of options and returns a list of just the words
	def options_to_words(self, options):
		words = list()
		for op in options:
			words.append(self.get_word(op).strip())
		return words	


	# postprocessing of the English sentences
	def polish(self, sentences):
		results = list()
		for sent in sentences:
			updated = self.reorder_adjectives(sent)
			updated = self.fix_a_an(updated)
			updated = self.fix_negation(updated)
			updated = self.fix_adj(updated)
			updated = self.options_to_words(updated)
			updated = self.dedup_and_separate(updated)
			results.append(updated)
		return results


	# choose best english sentence from a list of list of possible words
	def choose_best_sentence(self, sent_ops):
		if len(sent_ops) <= 0:
			return []
		sentences = self.generate_sentences(sent_ops)
		sentences = self.polish(sentences)
		best = self.get_best(sentences)
		string = ''
		for word in best:
			string += word + ' '
		print "BEST: " + string
		return best


	# correct issues like "a ella le gusta"
	def idiomatic_fix(self, sentence):
		sentence_str = ''
		for word in sentence:
			sentence_str += word + ' '
		final_str = ''
		regex = '(.*)(?:a|A)\(sps00\) ([A-z]{1,}\(.*\) ?[A-z]{0,}\(.*\)) le\(pp3csd00\) (?:gusta|encanta|gustan|encantan)(.*)'
		m = re.findall(regex, sentence_str)

		sentiment = ' likes(None) '
		for elem in m:
			if len(elem) == 3:
				final_str = elem[0] + elem[1] + sentiment + elem[2]
				return final_str.split()
			elif len(elem) == 2:
				final_str = elem[0] + sentiment + elem[1]
				return final_str.split()
		return sentence_str.split() # return an array split on spaces


	# replace common special cases with correct idiomatic translation
	def special_cases(self, sentence):
		sent = ''
		for word in sentence:
			sent += word + ' '
		sent = sent.replace('tuvo(vmis3s0) que(pr0cn000)', 'hadto(None)')
		sent = sent.replace('caso(ncms000) de(sps00)', 'caseof(None)')
		sent = sent.replace('sistema(ncms000) de(sps00)', 'systemof(None)')
		sent = sent.replace('en(sps00) hacer(vmn0000)', 'ofmaking(None)')
		sent = sent.replace('para que(pr0n000)', 'inorderto(None)')
		return sent.split()


	# basic direct translation
	def stupid_translate(self):
		for line in self.sentences:
			english_sentence = list()
			self.sentence_count += 1
			line = self.idiomatic_fix(line)
			line = self.special_cases(line)
			for i, word in enumerate(line):
                		next_word = line[i+1] if i != (len(line) - 1) else None 
				poss_words = self.translate(i, word, next_word)
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
				print line
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
