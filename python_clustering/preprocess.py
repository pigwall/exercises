import codecs 
import sys
from sklearn.feature_extraction.text import TfidfVectorizer

def get_iterms(filename):
	f = codecs.open(filename, 'r')
	lines = f.readlines()
	iterms= {}
	for i in xrange(len(lines)):
		parts = lines[i].split('\t');
		iterms[parts[0]] = parts[3].lower()
	return iterms

def trans2dict(raw_dict):
	dictionary = {}
	index = 0
	for key, value in raw_dict.iteritems():
		words = value.split(' ')
		for word in words:
			if word not in dictionary:
				dictionary[word] = index
				index += 1
	return dictionary

def trans2vector(raw_dict, dictionary):
	vect_dict = {}
	for key, value in raw_dict.iteritems():
		words = value.split(' ')
		vect = []
		for word in words:
			vect.append(dictionary[word])
		vect_dict[key] = vect
	return vect_dict

def wirte_tfidf(raw_dict, dictionary):
	
	return
def main(argv):
	raw_dict = get_iterms(argv[1])
	dictionary = trans2dict(raw_dict)
	vectors = trans2vector(raw_dict, dictionary)
	if argv[2] == 'tfidf':
		vectors = write_tfidf(raw_dict, dictionary)
	else:
		with codecs.open(argv[2],'w') as processed:
			for key, value in vectors.iteritems():
				vect = ' '.join(map(lambda x: str(x)+":1", value))
				processed.write(key + '\t' + vect + '\n')
	return
if __name__ == '__main__':
	main(sys.argv)