from langchain.text_splitter import RecursiveCharacterTextSplitter

class Papers(object): 
    def __init__(self, documents_dict):
        self.documents = []
        self.metadatas = []
        self.ids = []

        split_documents_dict = self.split_texts_in_dict(documents_dict)

        for key, value in split_documents_dict.items():
            metadata = self.create_metadata(value['title'], value['authors'], value['published'], value['link'])
            self.add(value['summary'], metadata, key)
    
    def add(self, document: str, metadata: dict, id: str):
        self.documents.append(document)
        self.metadatas.append(metadata)
        self.ids.append(id)
    
    def create_metadata(self, title: str, authors: str, published: str, link: str):
        metadata = {'title': title,
                    'authors': authors,
                    'published': published,
                    'link': link}
        return metadata

    def split_texts(self, texts: str, chunk_size: int = 1000, chunk_overlap: int = 100, length_function=len):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size,
            chunk_overlap  = chunk_overlap,
            length_function = length_function
            )
        return text_splitter.split_text(texts)

    def split_texts_in_dict(self, documents_dict: dict): 
        split_documents_dict = {}
        for key, value in documents_dict.items():
            summary = value['summary']
            split_summary = self.split_texts(summary)
            for n, chunk in enumerate(split_summary):
                split_documents_dict[key + f'_{n}'] = {'title': value['title'],
                                                    'authors': value['authors'],
                                                    'summary': chunk,
                                                    'published': value['published'],
                                                    'link': value['link']}
        return split_documents_dict

