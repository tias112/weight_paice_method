import spacy
from solr_client import SolrClient

class Stemmer:
    def __init__(self, solr, index = 'textsearch', fieldtype='fieldvalue', field = 'text_fr_z', name='default'):
        self.solr = solr
        self.index = index
        self.fieldtype = fieldtype
        self.field = field
        self.name = name
        
    def stem_word(self, word):
        list3 = self.solr.analysis(self.index, self.fieldtype, self.field, word)
        if list3:            
            return list3[0]
        return ""
    
    def stem_words(self, words):
        assert isinstance(words, list)
        return map(self.stem_word, words)

    def stem_text(self, words):
        stems = self.solr.analysis(self.index, self.fieldtype, self.field, words)
        if stems:            
            return dict(zip(words.split(' '), stems))
        return {}
    
class SpacyStemmer(Stemmer):
    def __init__(self, model, name='default'):
        self.nlp = spacy.load(model)
        self.name = name
        
    def stem_word(self, word):
        for token in self.nlp(word):
            return(token.lemma_)       
        return ""
    
    def stem_words(self, words):
        assert isinstance(words, list)
        return map(self.stem_word, words)
    
    def stem_text(self, words):
        return {token.text: token.lemma_ for token in self.nlp(words)}
    
class TruncateStem(Stemmer):
    def __init__(self, num):
        self.num = num
        self.name = 'TruncateStem{0}'.format(num)
        
    def stem_word(self, word):
        if len(word)<self.num:
            return ''
        return word[:-self.num]
    
    def stem_words(self, words):
        assert isinstance(words, list)
        return map(self.stem_word, words)