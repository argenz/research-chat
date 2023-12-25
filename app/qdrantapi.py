from qdrant_client import QdrantClient, models
from qdrant_client.http.models import PointStruct
from sentence_transformers import SentenceTransformer
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
import os
import uuid
import time
import pandas as pd 
import logging as log

log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


class QdrantAPI(object): 
    def __init__(self): 
        self.client = QdrantClient(url=os.getenv("QDRANT_API_URL"), 
            api_key=os.getenv("QDRANT_API_KEY"),)
        self.encoder = TextEmbeddingModel.from_pretrained("textembedding-gecko@002")
        self.EMBDEDDING_SIZE = 768 
             
#### Creating collection
    def create_collection(self, collection_name: str, recreate=False): 
        log.info(f"Creating collection: {collection_name}.")
        if recreate: 
            self.recreate_collection(collection_name=collection_name)
        else:
            self.create_collection_default(collection_name=collection_name)

    def create_collection_default(self, collection_name: str):
         self.client.create_collection(
                collection_name=collection_name, 
                vectors_config=models.VectorParams(
                    size=self.EMBDEDDING_SIZE, 
                    distance=models.Distance.COSINE,
                ),
            )
         
    def recreate_collection(self, collection_name: str):
         self.client.recreate_collection(
                collection_name=collection_name, 
                vectors_config=models.VectorParams(
                    size=self.EMBDEDDING_SIZE, 
                    distance=models.Distance.COSINE,
                ),
            )
         
## Handling index
    def insert_documents(self, collection_name: str, documents_dict: dict):              
            #idxs, embeddings, payloads = self.organize_upload(documents_dict)

            for num, item in enumerate(documents_dict.items()): 
                _, doc_dict = item 
                idx = str(uuid.uuid4())

                log.info(f"Embedding document {num}/{len(documents_dict.items())}.")

                text_embedding = self.get_embedding(doc_dict["summary"], isquery=False)
                
                log.info("Uploading point to Qdrant.")

                self.client.upsert(
                    collection_name=collection_name,
                    points=[
                            models.PointStruct(
                                id=idx,
                                payload=doc_dict,
                                vector=text_embedding,
                            ),
                    ],
                )
            
    # def organize_upload(self, documents_dict: dict): 
    #         embeddings = []
    #         idxs = []
    #         payloads = []

    #         for num, item in enumerate(documents_dict.items()): 
    #             _, doc_dict = item 
    #             idx = str(uuid.uuid4())

    #             log.info(f"Embedding document {num}/{len(documents_dict.items())}.")

    #             text_embedding = self.get_embedding(doc_dict["summary"], isquery=False)
                
    #             embeddings.append(text_embedding)
    #             idxs.append(idx)
    #             payloads.append(doc_dict)

    #         return idxs, embeddings, payloads

    
    def get_embedding(self, text: str, isquery=True): 
        try: 
            if isquery: task_type = "RETRIEVAL_QUERY"
            else: task_type = "RETRIEVAL_DOCUMENT"

            text_embedding_input = TextEmbeddingInput(task_type=task_type, text=text)
            embeddings = self.encoder.get_embeddings([text_embedding_input])
            return embeddings[0].values
        
        except:
            time.sleep(10)
            print("Vertex AI embeddings rate limit reacehd, waiting 10 seconds ...")
            return self.get_embedding(text, isquery)

# querying 
    def query_index(self, collection_name: str, query: str, k=10): 
        # TODO: if collection doesn't exist, create collection
        return self.client.search(
        collection_name=collection_name,
        query_vector=self.get_embedding(query).tolist(),
        limit=k,
        )
        

    
