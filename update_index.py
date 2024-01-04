# Step 1: 
# TODO: 1. Get new paper abstracts from axiv email subscription save them to csv. 
# 2. Parse abstracts and create index 
# 3. Have Fast API running on machine on updated version of index 
# 4. Have front end that answers question and shows source papers

from dotenv import load_dotenv
from app.index import Index
from datetime import datetime, timedelta
import logging as log

log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

load_dotenv()

category = 'cat:cs.IR'
collection_name = "information_retrieval"

index = Index()
log.info(f"Initialized index.")

#index.new_collection(collection_name, recreate=True)
#log.info(f"Created new collection.")

to_date = datetime.now() 
from_date = to_date - timedelta(days=365)

# add documents by month
index.add_abstracts_by_date(from_date, to_date, category, collection_name)
   
