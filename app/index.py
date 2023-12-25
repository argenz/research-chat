
from app.arxivapi import ArxivAPI
from app.qdrantapi import QdrantAPI
from dotenv import load_dotenv
from datetime import datetime, timedelta
from app.utils import split_texts_in_dict
import logging as log

log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

class Index(object): 
    def __init__(self):
        self.arxiv_api = ArxivAPI()
        self.qdrant_client = QdrantAPI()

    def add_abstracts_by_date(self, from_date: datetime, to_date: datetime, category: str, collection_name: str): 
        # get abstracts from API
        result = self.arxiv_api.get_abstracts(category, 
                          from_date=from_date.strftime('%Y%m%d')+"000000", 
                          to_date=to_date.strftime('%Y%m%d')+"000000")
        
        # split text
        result = split_texts_in_dict(result)

        # add to collection
        self.qdrant_client.insert_documents(collection_name=collection_name, documents_dict=result)
    
    def add_yesterdays_abstracts(self, category: str, collection_name: str): 
        to_date = datetime.now()
        from_date = to_date - timedelta(days=1)

        self.add_abstracts_by_date(from_date, to_date, category, collection_name)

    def new_collection(self, collection_name, recreate: bool=False):
        self.qdrant_client.create_collection(collection_name, recreate)

    