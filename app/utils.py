from langchain.text_splitter import RecursiveCharacterTextSplitter
import re

def split_texts_in_dict(documents_dict: dict): 
    split_documents_dict = {}
    for key, value in documents_dict.items():
        summary = value['summary']
        split_summary = split_texts(summary)
        for n, chunk in enumerate(split_summary):
            split_documents_dict[key + f'_{n}'] = {'title': value['title'],
                                                'authors': value['authors'],
                                                'summary': chunk,
                                                'published': value['published'],
                                                'link': value['link']}
    return split_documents_dict

def split_texts(texts: str, chunk_size: int = 500, chunk_overlap: int = 50, length_function=len):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap  = chunk_overlap,
        length_function = length_function
        )
    return text_splitter.split_text(texts)

def clean_text(text): 
     pattern = r'["\'{}]'
     return re.sub(pattern, '', text)
