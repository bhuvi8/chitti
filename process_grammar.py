import pickle
import logging
from operator import itemgetter
from location_solver import locationSolve
from search import Query
from utils.www_desc_finder import DescLookup
from utils.language_processor import *
 
logger = logging.getLogger(__name__)

class RuleProcessor:
    def __init__(self):
        self.www_lookup = DescLookup()
        self.loc_solver = locationSolve()
        self.find = Query()
        self.coarse_classifier_obj = 'data/q_coarse_classifier.pickle'
        self.fine_classifier_obj = 'data/q_fine_classifier.pickle'
        self.qstn_coarse_classifier = pickle.load(open(self.coarse_classifier_obj, 'rb'))
        self.qstn_fine_classifier = pickle.load(open(self.fine_classifier_obj, 'rb'))
        self.qstn_coarse_classes = ['LOC', 'DESC', 'ENTY', 'ABBR', 'NUM', 'HUM']
        self.qstn_fine_classes = ['def', 'abb', 'event', 'dist', 'mount', 'word', 'color', 'gr', 'dismed', 'product', 'file', 'period', 'temp', 'animal', 'desc', 'sport', 'currency', 'volsize', 'letter', 'directory', 'money', 'code', 'symbol', 'instru', 'title', 'techmeth', 'count', 'date', 'reason', 'manner', 'state', 'city', 'perc', 'ord', 'religion', 'lang', 'weight', 'country', 'plant', 'cremat', 'food', 'ind', 'exp', 'veh', 'substance', 'body', 'speed', 'termeq', 'other']
        
    def query_analyzer(self,q,ip):
        query_type = ''
        res = ''
        res = self.classify_query(q,ip)
        if not res:
            return 'Nothing found'
        return res

    def classify_query(self,postgq,ip):
        res = ''
        tmp_res = ''
        srch_trm = ''
        count = 0
        cc,fc = self.classify_qstn_type(postgq)
        res = self.qstn_solve_chooser(cc,fc,postgq,ip)
        if not res:
            srch_trm = find_chunk(postgq)
            logger.debug('www search_term %s' %srch_trm)
            if (srch_trm) and (len(srch_trm) >= 3) :
                res += self.www_lookup.get_data(srch_trm)
        if not res:
            srch_trm = find_chunk(postgq,'DCHUNK: <W.*>?<V.*>*?{<.*>*?}<\.>')
            logger.info('SEngine:'+ srch_trm)
            res,res_list = self.find.search(srch_trm)
        return res
    
    def classify_qstn_type(self,pos_sent):
        qstn_c_prob = {}
        qstn_f_prob = {}
        features = self.qstn_feature_extractor_v2(pos_sent)
        #coarse class classifier
        qstn_c_prob_dist = self.qstn_coarse_classifier.prob_classify(features)
        #for information only
        for label in self.qstn_coarse_classifier.labels():
            qstn_c_prob[label] = qstn_c_prob_dist.logprob(label)
        logger.info(sorted(qstn_c_prob.items(), key=itemgetter(1), reverse=True)[:3])
        
        qstn_c_class = qstn_c_prob_dist.max()
        features['coarse'] = qstn_c_class
        #fine class classifier
        qstn_f_prob_dist = self.qstn_fine_classifier.prob_classify(features)
        for label in self.qstn_fine_classifier.labels():
            qstn_f_prob[label] = qstn_f_prob_dist.logprob(label)
        logger.info(sorted(qstn_f_prob.items(), key=itemgetter(1), reverse=True)[:3])
        
        qstn_f_class = qstn_f_prob_dist.max()
        return qstn_c_class,qstn_f_class
        
    def qstn_feature_extractor_v2(self,pos_sent):
        features={}
        for (w,t) in pos_sent:
            if t.startswith('W'): #or w == 'EX':
                features['qstn_word'] = w.lower()
        features['question_focus'] = find_chunk(pos_sent)        
        features['pos_tags'] = ' '.join([ a[1] for a in pos_sent ])
        features['1st verb'] = find_chunk(pos_sent,'VCHUNK: <.*>*?{<V.*>+}<.*>*')
        return features
        
    def fine_feature_extractor(self,pos_sent):
        features = self.qstn_feature_extractor_v2(pos_sent)
        coarse = self.qstn_fine_classifier.classify(features)
        self.features['coarse'] = coarse
        return (features)
    
    def qstn_solve_chooser(self,cc,fc,postgq,ip):
        res = ''
        if cc == 'DESC' and fc == 'def':
            srch_trm = find_chunk(postgq,'DCHUNK: <W.*><V.*><DT>*{<V.*>*<RB.*>*<JJ>*<N.*>*}')
            if srch_trm:
                res = self.www_lookup.get_data(srch_trm,fc)
        elif cc == 'LOC':
            res = self.loc_solver.loc_solve_chooser(fc,postgq,ip)
        return res

