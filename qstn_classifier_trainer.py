import pickle
import nltk

#download nltk qc corpus using nlt.download() 	
def find_chunk(sent,chunk_rule=None):
	if not chunk_rule: 
		chunk_rule = 'HCHUNK: <W.*><.*>*?{<N.*>+}'
	label=chunk_rule.split(':')[0].strip()
	cp = nltk.RegexpParser(chunk_rule)
	tree = cp.parse(sent)
	for subtree in tree.subtrees():
		if subtree.label() == label:
			subtree = ' '.join([a[0] for a in subtree ])
			print (subtree)
			return subtree
##this is required only once		
from os.path import expanduser
qc_corpora = expanduser("~") + '/nltk_data/corpora/qc/'
#pre process train.txt dataset
train_qc = open(qc_corpora + 'train.txt' ,'r').readlines()
train_qc = [ i.strip() for i in train_qc ]
res = pos_tag_questions(train_qc)
pickle.dump(res, open("data/qc_train_data_pos_tag.pickle","wb"))
#pre process test.txt dataset
test_qc = open(qc_corpora + 'test.txt' ,'r').readlines()
test_qc = [ i.strip() for i in test_qc ]
res = pos_tag_questions(test_qc)
pickle.dump(res, open("data/qc_test_data_pos_tag.pickle","wb"))
#pos tagging is resource intensive so do it once and save the result
#as a pickle object for future uses
def pos_tag_questions(qstn_list):
	res = []
	count = 0 
	for i in qstn_list:
		r = []
		i = i.split(':')
		r.append(i[0])
		r.append(i[1].split()[0])
		i = i[1].split()
		del i[0]
		sent = nltk.word_tokenize(' '.join(i))
		r.append(nltk.pos_tag(sent))
		res.append(tuple(r))
		count += 1
		if (count % 100) == 0:
			print ("processed : " + str(count) )
	return res

#experiment with different features to get better accuracy
#also dont forget to to include the same feature extractor in the process_grammar.py
def qstn_feature_extractor(sent):
	features={}
	for (w,t) in sent:
		if t.startswith('W'): #or w == 'EX':
			features['qstn_word'] = w.lower()
	features['question_focus'] = find_chunk(sent)		
	features['pos_tags'] = ' '.join([ a[1] for a in sent ])
	features['1st verb'] = find_chunk(sent,'VCHUNK: <.*>*?{<V.*>+}<.*>*')
	return features
	
def fine_data_v2(c,f,q):
	features = qstn_feature_extractor(q)
	coarse = coarse_classifier.classify(features)
	features['coarse'] = coarse
	return (features,f)
	
qst = pickle.load(open("data/qc_train_data_pos_tag.pickle", 'rb'))
tst = pickle.load(open("data/qc_test_data_pos_tag.pickle", 'rb'))
qst_coarse = [ (c,q) for (c,f,q) in qst]
qst_coarse_features = [ (qstn_feature_extractor(q),c) for (c,f,q) in qst_coarse]
coarse_classifier = nltk.NaiveBayesClassifier.train(qst_coarse_features)
tst_coarse = [ (c,q) for (c,f,q) in tst]
tst_coarse_features = [ (qstn_feature_extractor(q),c) for (c,f,q) in tst_coarse]
nltk.classify.accuracy(coarse_classifier, tst_coarse_features)
pickle.dump(fine_classifier, open("data/q_coarse_classifier.pickle","wb"))
	
fine_train_data = [ fine_data(c,f,q) for (c,f,q) in qst]
fine_classifier = nltk.NaiveBayesClassifier.train(fine_train_data)
del fine_train_data
fine_test_data = [ fine_data(c,f,q) for (c,f,q) in tst]
nltk.classify.accuracy(fine_classifier, fine_test_data)
pickle.dump(fine_classifier, open("data/q_fine_classifier.pickle","wb"))
