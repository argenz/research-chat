from qdrant_client import QdrantClient, models
from sentence_transformers import SentenceTransformer
import os
import uuid


class QdrantAPI(object): 
    def __init__(self): 
        self.client = QdrantClient(url=os.getenv("QDRANT_API_URL"), 
            api_key=os.getenv("QDRANT_API_KEY"),)
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')

    def create_collection(self, collection_name: str, recreate=False): 
        if recreate: 
            self.recreate_collection(collection_name=collection_name)
        else:
            self.create_collection_default(collection_name=collection_name)

    def create_collection_default(self, collection_name: str):
         self.client.create_collection(
                collection_name=collection_name, 
                vectors_config=models.VectorParams(
                    size=self.encoder.get_sentence_embedding_dimension(), 
                    distance=models.Distance.COSINE,
                ),
            )
         
    def recreate_collection(self, collection_name: str):
         self.client.recreate_collection(
                collection_name=collection_name, 
                vectors_config=models.VectorParams(
                    size=self.encoder.get_sentence_embedding_dimension(), 
                    distance=models.Distance.COSINE,
                ),
            )

    def insert_documents(self, collection_name: str, documents_dict: dict):             
            self.client.upload_records(
                    collection_name=collection_name,
                    records=[
                        models.PointStruct(
                            id=str(uuid.uuid4()), vector=self.encoder.encode(doc_dict["summary"]), payload=doc_dict
                        )
                        for _, doc_dict in documents_dict.items()
                    ],
                )

    def query_index(self, collection_name: str, query: str, k=10): 
        # TODO: if collection doesn't exist, create collection
        return self.client.search(
        collection_name=collection_name,
        query_vector=self.encoder.encode(query).tolist(),
        limit=k,
        )
        

    
