class Translator:

	def __init__(self):
		self.dictionary = dict()
		self.sentences = list()
		self.translation = list()

	# starter function to look up a word (later make more complicated/intelligent)
	def translate(self, word):
		print word
		options = self.dictionary[word.lower()]
		return options[0] # this can be modified later to not just use the first translation option

	# basic direct translation
	def stupid_translate(self):
		for line in self.sentences:
			english_sentence = list()
			for word in line:
				print word
				#english_word = self.translate(word)
				#print english_word
				#english_sentence.append(english_word)
				#self.translation.append(english_sentence)

	# read in a file and convert into usable form
	def read_file(self, file_name):
		contents = list()
		f = open(file_name)
		for line in f:
			contents.append(line)
		f.close()
		full = '\n'.join(contents)
		result = full.split()
		return result

	# reads in our mini dictionary and makes usable
	def parse_dict(self, dictionary):
		f = open(dictionary)
		for line in f:
			split = line.split(':')
			if len(split) == 2:
				key = split[0] # spanish word
				values = split[1].split(',') # multiple possible english words for a single spanish word
				print key
				print values
				self.dictionary[key] = values
			else:
				print split # if anything prints, there's a problem with the dictionary

def main():
	sentences_file = 'data/sentences.txt'
	dictionary_file = 'data/dictionary.txt'
	t = Translator()
	t.parse_dict(dictionary_file)
	t.sentences = t.read_file(sentences_file)
	t.stupid_translate()

if __name__ == '__main__':
	main()