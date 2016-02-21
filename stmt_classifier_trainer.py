import nltk
import pickle
#reuires nltk chat corpus, download it using nltk.download()
#create a statement classifier from nltk chat corpus
#try and experiment with different feature sets to get better classifer
#also remember to use the same featureset function in the statement_classifier.py
posts = nltk.corpus.nps_chat.xml_posts()
posts = [ a for a in posts if a.get('class') != 'System' ]
def dialogue_act_features(post):
	features = {}
	pos_l = []
	first = True
	if isinstance(post,str):
		tokens = nltk.word_tokenize(post)
		postg = nltk.pos_tag(tokens)
		for (w,t) in postg:
			if first:
				features['starts_with'] = w.lower()
				first = False
				continue 
			features['contains(%s)' % w.lower()] = True
			pos_l.append(t)
	else:		
		for word in post.getchildren():
			for t in word.getchildren():
				pos = t.get('pos')
				word = t.get('word')
				pos_l.append(pos)
				if first:
					features['starts_with'] = word.lower()
					first = False
					continue
				features['contains(%s)' % word.lower()] = True
	features['pos'] = ' '.join(pos_l)
	return features

featuresets = [(dialogue_act_features(post), post.get('class')) for post in posts]
size = int(len(featuresets) * 0.1)
train_set, test_set = featuresets[size:], featuresets[:size]
classifier = nltk.NaiveBayesClassifier.train(train_set)
print (nltk.classify.accuracy(classifier, test_set))
pickle.dump(res,open("data/stmnt_classifier.pickle","wb"))

