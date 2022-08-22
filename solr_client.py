
import os
import urllib
import requests


class SolrClient:
    def __init__(self, host, port):
        self.docker = os.environ.get('LTR_DOCKER') != None
        self.solr = requests.Session()
        self.username = "solr"
        self.password = "solr"

        if self.docker:
            self.host = 'solr'
            self.solr_base_ep = 'http://solr:8983/solr'
        else:
            self.host = host
            self.port = port
            self.solr_base_ep = 'http://{}:{}/solr'.format(self.host, self.port)

    def get_host(self):
        return self.host
    
    def auth(self, user, pwd):
        self.username = user
        self.password = pwd
            
    def search(self, index, query, lang):
        params = {
            'q': query,
            'wt': 'json',
            'df': 'id',
            'rows': 10,
            'user.country': 'test',
            'user.company': 'test',
            'user.customer': 'test',
            'user.companymarket': 'test',
            'textquery.query': lang
        }
        resp = requests.get('{}/{}/select'.format(self.solr_base_ep, index), params=params, auth=(self.username, self.password))

        response = resp.json()
       
        txt_response = response['textquery.response']
        ids = []
        for doc in txt_response['docs']:
            ids.append(doc['id'])
        return {
            'numFound': txt_response['numFound'],
            'ids': ids
        }
    def add_symetric_syn(self, index, managed, words):
        body = words
        resp = requests.put('{}/{}/schema/analysis/synonyms/{}'.format(self.solr_base_ep, index, managed), json=body, auth=(self.username, self.password))          
        print('add symetric ', managed, words)
        return  resp.json()

    def add_asymetric_syn(self, index, managed, target, words):
        body = { target : words }
        resp = requests.put('{}/{}/schema/analysis/synonyms/{}_asymetric'.format(self.solr_base_ep, index, managed), json=body, auth=(self.username, self.password))          
        print('add asymetric ', managed,target, words)
        return  resp.json()

    def analysis(self, index, analyze_type, field, words):
        
        field_anlsis = 'analysis.{}'.format(analyze_type)
    
        params = {
            'wt': 'json',
            'analysis.showmatch': 'true',
            field_anlsis: words,
            'analysis.fieldtype':  field
        }
        resp = requests.get('{}/{}/analysis/field'.format(self.solr_base_ep, index), params=params, auth=(self.username, self.password))
        
        response = resp.json()
       
        atype = 'index'
        if analyze_type in ['query']:
            atype='query'
        
        filters = response['analysis']['field_types'][field][atype]
        
        return [doc['text'] for doc in filters[-1]]
    
def main():    
    g = SolrClient(8986)
    print(g.search('textsearch', 'massey ferguson 135'))


if __name__ == "__main__":
    main()