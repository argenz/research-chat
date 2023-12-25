import urllib, urllib.request
import feedparser
import logging as log 
import json
from app.utils import clean_text

log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class ArxivAPI(object): 
    def __init__(self):
        self.url = f'http://export.arxiv.org/api/query?'

    def get_abstracts(self, search_query, from_date, to_date, start=0, max_results=10000):
        response = self.search_cat(search_query, from_date, to_date, start, max_results)
        abstracts = self.xml_to_dict(response)
        return abstracts

    def search_cat(self, search_query, from_date, to_date, start, max_results):
        query = 'search_query=%s+AND+submittedDate:[%s+TO+%s]&start=%i&max_results=%i' % (search_query, 
                                                            from_date, 
                                                            to_date,
                                                            start,
                                                            max_results)
        full_url = self.url+query
        log.info('Querying arXiv API with: %s', full_url)
        return urllib.request.urlopen(full_url).read().decode('utf-8')
    
    def xml_to_dict(self, response_xlm):
        ''' Parse the xml response from the arxiv api into a dictionary with keys arxiv id 
        and values a dictionary with the paper information: title, authors, summary, published, doi
        '''
        response_dict = {}
        feed = feedparser.parse(response_xlm)

        for entry in feed.entries:
            response_dict[entry.id.split('/abs/')[-1]] = {'title': clean_text(entry.title),
                                                          'authors': clean_text(entry.author),
                                                          'summary': clean_text(entry.summary),
                                                          'published': entry.published,
                                                          'link': entry.link,
                                                          'id': entry.id.split('/abs/')[-1]}    
        
        #self.to_json(response_dict, "arxiv-download")
        return response_dict
    
    # def to_json(self, response_dict, filename): 
    #     with open(f'{filename}.json', 'w') as f:
    #         # write the dictionary to the file in JSON format
    #         json.dump(response_dict, f)
    #     log.info("JSON saved.")
    
    

