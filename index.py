
import chromadb

class Index(object): 
    def __init__(self, persist_dir, collection_name) -> None:
        self.persist_dir = persist_dir
        self.index = self.load_index(collection_name)

    def load_index(self, collection_name):
        client = chromadb.PersistentClient(path=self.persist_dir)
        index = client.get_or_create_collection(name=collection_name)
        return index
    
    def add_documents(self, documents: list[str], metadatas: dict, ids: list[str]):
        # embeddings computed with sentence transformers by default
        # add embedding parameter here in case this changes in the future
        self.index.add(documents=documents, metadatas=metadatas, ids=ids)

    def query_index(self, query_texts: list[str], k=10, metadata_filter=None, content_filter=None):
        ''' Query the index with a list of query texts and return the top k results.
        '''
        return self.index.query(
                        query_texts=query_texts,
                        n_results=k,
                        where=metadata_filter, #{"metadata_field": "is_equal_to_this"}
                        where_document=content_filter # {"$contains":"search_string"}
                    )
    
