import nltk
import logging

logger = logging.getLogger(__name__)

def pos_tag_sent(sent):
    tokens = nltk.word_tokenize(sent)
    postg = nltk.pos_tag(tokens)
    return postg


def find_chunk(sent, chunk_rule=None):
    if not chunk_rule: 
        chunk_rule = 'QWORD: <W.*><V.*><DT>*{<.*>*?<N.*>+}'
    logger.debug(chunk_rule)
    label=chunk_rule.split(':')[0].strip()
    cp = nltk.RegexpParser(chunk_rule)
    tree = cp.parse(sent)
    for subtree in tree.subtrees():
        if subtree.label() == label:
            subtree = ' '.join([a[0] for a in subtree ])
            return subtree

def find_named_entities(sent):
    tree = nltk.ne_chunk(sent)
    for st in tree.subtrees():
        if st.label() != 'S':
            logger.debug(st)
