from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score
import sys
import codecs 
import numpy as np 
from scipy.sparse import csr_matrix
from itertools import groupby
import math

def readin_matrix(filename):
	f = codecs.open(filename, 'r')
	lines = f.readlines()
	A, B, C = [], [], []
	index_dict = {}
	for i in xrange(len(lines)):
		parts = lines[i].split('\t')
		index_dict[i] = parts[0]
		indexes = parts[1].split(' ')
		for ind in indexes:
			B.append(i)
			A.append(int(ind))
			C.append(1.0)
	max_word = max(A) + 1
	max_iterm = max(B) + 1
	matrix = csr_matrix((C, (B, A)), dtype = float, shape=(max_iterm, max_word))
	return index_dict, matrix

def readin_X(filename):
	f = codecs.open(filename, 'r')
	lines = f.readlines()
	index_dict = {}
	matrix = {}
	for i in xrange(len(lines)):
		parts = lines[i].split('\t')
		index_dict[i] = parts[0]
		scores = parts[1].split(' ')
		vect_dict = {}
		for score in scores:
			vect_dict[int(score.split(":")[0])] = float(score.split(":")[1]) 
		matrix[i] = vect_dict
	return index_dict, matrix

def get_mod(vect):
	dot = 0.0
	for key, val in vect.iteritems():
		dot = dot + vect[key]*vect[key]
	return math.sqrt(dot)

def compute_cosine(cur_vect, vect):
	dot = 0.0
	for key, value in cur_vect.iteritems():
		if key in vect:
			dot = dot + cur_vect[key] * vect[key]
	mod_cur = get_mod(cur_vect)
	mod_vec = get_mod(vect)
	return dot / (mod_cur * mod_vec)

def put(top10, cosine, i):
	if cosine == 1.0:
		return
	if len(top10) < 10:
		top10[i] = cosine
	else:
		index = max(top10, key=lambda x: top10[x])
		top10.pop(index)
		top10[i] = cosine
	return

def find10(cur_vect, matrix, iterm_num):
	top10 = {}
	for i in xrange(iterm_num):
		vect = matrix[i]
		cosine = compute_cosine(cur_vect,vect)
		put(top10, cosine, i)
	return top10

def put_all(tops, cosine, i):
	if cosine > 0.3 and cosine < 1.0:
		tops[i] = cosine
	return
def find(cur_vect, matrix, iterm_num):
	tops = {}
	for i in xrange(iterm_num):
		vect = matrix[i]
		cosine = compute_cosine(cur_vect,vect)
		put_all(tops, cosine, i)
	return tops

def output_ex1(index_dict, matrix, filename):
	sim_dict = {}
	iterm_num = len(index_dict)
	for key, val in index_dict.iteritems():
		if key > 100:
			break
		cur_vect = matrix[key]
		cur_sim_dict = find10(cur_vect, matrix, iterm_num)
		sim_dict[key] = cur_sim_dict

	with codecs.open(filename,'w') as pridictions:
		for key, value in sim_dict.iteritems():
			predictions.wirte(index_dict[key] + "\t")
			for k, v in value:
				predictions.wirte(index_dict[k] + ' ')
			predictions.wirte('\n')
	return 

def output_ex2(index_dict, matrix, filename):
	sim_dict = {}
	iterm_num = len(index_dict)
	for key, val in index_dict.iteritems():
		cur_vect = matrix[key]
		cur_sim_dict = find(cur_vect, matrix, iterm_num)
		sim_dict[key] = cur_sim_dict
	return

def cluster2index(y):
	cluster_dict = {}
	for i in xrange(len(y)):
		clusterid = y[i]
		if clusterid in cluster_dict:
			cluster_dict[clusterid].appnend(i)
		else:
			cluster_dict[clusterid] = [i]
	return cluster_dict

def main(argv):
	index_dict, X = readin_X(argv[1])
	#true_k = 500
	if argv[2] == 'ex1':
		output_ex1(index_dict, X, argv[3])
		return
	#else:
	#	output_ex2(index_dict, X, argv[3])

	index_dict, X = readin_matrix(argv[1])
	#vectorizer = TfidfVectorizer(stop_words='english')
	#print X
	#X = vectorizer.fit_transform(documents)
	# x is a sparse vector turn to numpy
	model = KMeans(n_clusters=true_k, init='k-means++', max_iter=100, n_init=1)
	print 'training....\n'
	model.fit(X)
	print 'predicting....\n'
	y = model.predict(X)
	cluster_dict = cluster2index(y)
	#s = model.
	#print("Top terms per cluster:")
	#print len(y)
	#result = [len(list(group)) for key, group in groupby(y)]
	with codecs.open(argv[3],'w') as processed:
		for key, value in index_dict:
			processed.wirte(index)
			
		processed.write(str(b) + '\n')

	
	#if argv[2] == 'ex1':
	#	output_ex1(y, index_dict, X, cluser_dict, argv[3])
	#else
	#	output_ex2(y, index_dict, cluster_dict, argv[3])
	#count to see
	#output(y, index_dict, argv[2])
	#output the similar clusters

	#order_centroids = model.cluster_centers_.argsort()[:, ::-1]
	#terms = vectorizer.get_feature_names()
	#for i in range(true_k):
	#	print "Cluster %d:" % i,
	#	for ind in order_centroids[i, :10]:
	#		print ' %s' % terms[ind],
	#	print
	#X = readin_X(argv[1])
	#model = KMeans(n_clusters=)
	return
if __name__ == '__main__':
	main(sys.argv)