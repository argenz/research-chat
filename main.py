# Step 1: 
# TODO: 1. Get new paper abstracts from axiv email subscription save them to csv. 
# 2. Parse abstracts and create index 
# 3. Have Fast API running on machine on updated version of index 
# 4. Have front end that answers question and shows source papers

from arxivapi import ArxivAPI
from index import Index

category = 'cat:cs.IR'

api = ArxivAPI()
index = Index(persist_dir=f'./chromadb', collection_name='information_retrieval')

#papers = api.get_papers(category, max_results=100)
#index.add_documents(documents=papers.documents, metadatas=papers.metadatas, ids=papers.ids)

result = index.query_index(query_texts=['information retrieval'], k=10)

print(result) 
print(result.keys())
print(result['metadatas'])
print(result['documents'])
print(sum(len(doc) for doc in result['documents'][0])/len(result['documents'][0]))