import pickle
import logging
from operator import itemgetter
from process_grammar import RuleProcessor
from search import Query
from db_api.db_chat import ChatDB
from utils.language_processor import *

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)


class StmtClassify:
    def __init__(self):
        self.qry = RuleProcessor()
        self.db_con = ChatDB()
        self.find = Query()
        self.statement_types = {'Emotion' : '_emotion',
                     'whQuestion' : '_whquestion',
                     'yAnswer' : '_yanswer',
                     'Reject' : '_reject',
                     'Emphasis' : '_emphasis',
                     'Greet' : '_greet',
                     'Statement' : '_statement',
                     'Other' : '_other',
                     'Clarify' : '_clarify',
                     'Bye' : '_bye',
                     'Accept' :'_accept',
                     'ynQuestion' : '_ynquestion',
                     'nAnswer' : '_nanswer',
                     'Continuer' : '_continuer' }
        self.classifier_obj = 'data/stmnt_classifier.pickle'
        #self.classifier_obj = 'data/q_fine_classifier.pickle'
        self.classifier = pickle.load(open(self.classifier_obj, 'rb'))
        
    def classify(self,q_obj):
        pos_tagged_q = pos_tag_sent(q_obj['q'])
        logger.debug(pos_tagged_q)
        features = self.stmt_features_extract(pos_tagged_q)
        logger.debug(features)
        statement_prob = {}
        prob_dist = self.classifier.prob_classify(features)
        #for information only
        for label in self.classifier.labels():
            statement_prob[label] = prob_dist.logprob(label)
        logger.info(sorted(statement_prob.items(), key=itemgetter(1), reverse=True)[:3])
        
        stmt_class = prob_dist.max()
        #insert labelled statement to db for training
        self.add_to_db(pos_tagged_q,stmt_class)
        res = self.process_classified_stmts(pos_tagged_q,stmt_class,q_obj['ip'])
        return res
        
    def stmt_features_extract(self,tagged_stmt):
        features = {}
        pos_l = []
        first = True
        for (w,t) in tagged_stmt:
            pos_l.append(t)
            if first:
                features['starts_with'] = w.lower()
                first = False
                continue 
            features['contains(%s)' % w.lower()] = True
        features['pos'] = ' '.join(pos_l)
        return features

    def stmt_features_extract_old(self,tagged_stmt):
        features = {}
        pos_l = []
        for (w,t) in tagged_stmt:
            features['contains(%s)' % w.lower()] = True
            pos_l.append(t)
        features['pos'] = ' '.join(pos_l)
        return features
        
    def add_to_db(self,tagged_stmt,label):
        stmt_doc = {}
        pos_l = []
        word_l = []
        for (w,t) in tagged_stmt:
            word_l.append(w)
            pos_l.append(t)
        stmt_doc['tokens'] = word_l
        stmt_doc['pos_tags'] = pos_l
        stmt_doc['class'] = label
        #insert to db
        stmt_id = self.db_con.insert_stmt(stmt_doc)
        if stmt_id:
            logger.info(stmt_id)
        
    def process_classified_stmts(self,tagged_stmt,label,ip):
        res = ''
        func_name = 'stmt' + self.statement_types[label]
        try:
            self.func = getattr(self, func_name)
        except AttributeError:
            logger.exception("Function not found: " + func_name)
        else:
            if label == 'whQuestion':
                res = self.func(tagged_stmt,ip)
            else:
                res = self.func(tagged_stmt)
        return res
    
    #functions for each of identifiable emotions
    def stmt_emotion(self,tagged_stmt):
        #TODO:understand +/-ve emotions and reply accordingly
        return 'I wish I could understand your feelings'
    def stmt_whquestion(self,tagged_stmt,ip):
        return  self.qry.query_analyzer(tagged_stmt,ip)
    def stmt_continuer(self,tagged_stmt):
        return  'Then whats next?'
    def stmt_emphasis(self,tagged_stmt):
        return  'ok ok I get it'
    def stmt_greet(self,tagged_stmt):
        return  'Hey Hi'
    def stmt_bye(self,tagged_stmt):
        return  'Bye Catch you later'
    def stmt_statement(self,tagged_stmt):
        srch_trm = find_chunk(tagged_stmt,'DCHUNK: {<.*>*}<\.>?')
        logger.info ('SEngine:'+srch_trm)
        res,junk = self.find.search(srch_trm)
        return  res
    def stmt_other(self,tagged_stmt):
        srch_trm = find_chunk(tagged_stmt,'DCHUNK: {<.*>*}<\.>?')
        logger.info ('SEngine:'+ srch_trm)
        res,junk = self.find.search(srch_trm)
        return  res
    def stmt_clarify(self,tagged_stmt):
        srch_trm = find_chunk(tagged_stmt,'DCHUNK: {<.*>*}<\.>?')
        logger.info ('SEngine:'+srch_trm)
        res,junk = self.find.search(srch_trm)
        return  res
    def stmt_ynquestion(self,tagged_stmt):
        srch_trm = find_chunk(tagged_stmt,'DCHUNK: {<.*>*}<\.>?')
        logger.info ('SEngine:'+srch_trm)
        res,junk = self.find.search(srch_trm)
        return  res
    def stmt_yanswer(self,tagged_stmt):
        return  'Acknowledgement accepted'
    def stmt_nanswer(self,tagged_stmt):
        return  'Ok thats fine with me'
    def stmt_accept(self,tagged_stmt):
        return  'Thank you for Acknowledging'
    def stmt_reject(self,tagged_stmt):
        return  'Why not?'

