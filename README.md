# Chat with Research papers 
This app is a chatbot over abstracts from papers published in 2023 on arXiv cs.IR subject field. It is structred as follows

app/
- arxivapi.py handles handles Arxiv api calls to retrieve and format the abstracts and metadata about the papers.
- qdrantapi.py handles the embedding of abstracts and insertion of entries in a qdrant collection, as well as collection creation, 
- index.py is an additional level of abstraction over arxivapi.py and qdrantapi.py to seamlessly create the index.
- vertexapi.py handles the calls to chat-Bison, text-Bison for LLM completions.
- utils.py contains text splitting, cleaning and iterator utils.
- requirements.txt contains the required packages.

create_index.py is the file I ran to create the index. TODO: create recurring jobs to add new papers periodically. 
