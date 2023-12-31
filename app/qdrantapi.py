from qdrant_client import QdrantClient, models
from vertexai.language_models import TextEmbeddingInput, TextEmbeddingModel
from utils import chunked
import os
import uuid
import time
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
    def insert_batch(self, collection_name: str, documents_batch: dict):              
            points = []
            i = 1 #TBR
            for _, doc_dict in documents_batch:

                log.info(f"Embedding document {i}/{len(documents_batch)}.") #TBR
                i += 1 #TBR

                idx = str(uuid.uuid4())
                text_embedding = self.get_embedding(doc_dict["summary"], isquery=False)
                points.append(models.PointStruct(id=idx, vector=text_embedding, payload=doc_dict))
                
            log.info("Uploading points to Qdrant.")
            self.upsert_to_qdrant(collection_name, points)

    def upsert_to_qdrant(self, collection_name, points): 
        try: 
            self.client.upsert(
            collection_name=collection_name,
            points=points
            ) 
        except Exception as e:
            log.info(f"Probably response handling exception: {e}")
            log.info(f"Trying again...")
            self.upsert_to_qdrant(collection_name, points)


    def insert_documents(self, collection_name: str, documents_dict: dict, batch_size=8):
        batch_n = 1 #TBR
        for chunk in chunked(documents_dict.items(), batch_size): 
            log.info(f"Inserting batch {batch_n}/{int(len(documents_dict)/batch_size)}") #TBR
            self.insert_batch(collection_name, chunk)
            batch_n += 1 #TBR
        
    
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
        query_vector=self.get_embedding(query),
        limit=k,
        )
        

    
