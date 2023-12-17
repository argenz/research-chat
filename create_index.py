
from arxivapi import ArxivAPI
from qdrantapi import QdrantAPI
from dotenv import load_dotenv
from datetime import datetime, timedelta
from utils import split_texts_in_dict

load_dotenv()
category = 'cat:cs.IR'

api = ArxivAPI()
qdrant_client = QdrantAPI()
to_date = datetime.now()
from_date  = to_date -  timedelta(days=300)

result = api.get_abstracts(category, 
                           from_date=from_date.strftime('%Y%m%d')+"000000", 
                           to_date=to_date.strftime('%Y%m%d')+"000000")
print(len(result))

result = split_texts_in_dict(result)
print(len(result))


qdrant_client.create_collection(collection_name='information_retrieval', recreate=True)
qdrant_client.insert_documents(collection_name='information_retrieval', documents_dict=result)