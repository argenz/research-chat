import streamlit as st
from arxivapi import ArxivAPI
from qdrantapi import QdrantAPI
from vertexapi import VertexAPI
from dotenv import load_dotenv
from prompts import context_prompt
import logging as log
import os


load_dotenv()

log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


# intialize vertex AI SDK and arxiv API
vertex_api = VertexAPI()
arxiv_api = ArxivAPI()
vertex_api.start_chat_session(context_prompt=context_prompt)
qdrant_client = QdrantAPI()

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chat over the latest papers in cs.IR on Arxiv.")
st.caption("🚀 A streamlit chatbot")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"author": "AI", "content": "Hi, I'm a chatbot that has access to all abstracts of Arxiv Papers submitted since Feb 2023 in the subject field of Information Retrieval (cs.IR). What would you like to explore?"}]

for msg in st.session_state.messages:
    st.chat_message(msg["author"]).write(msg["content"])

if prompt := st.chat_input():

    # semantic search and get most relevant paragraphs
    hits = qdrant_client.query_index(collection_name='information_retrieval', query=prompt, k = 20)

    # RAG format context
    context = []
    for hit in hits: 
        payload = hit.payload 
        context.append(f'Abstract: {payload["summary"]} - About the paper: {dict((k, payload[k]) for k in ("authors", "link", "published", "title"))}')

    context = '\n\n'.join(context)
    context_prompt = context_prompt.format(context=context)

    # get completion
    log.info(f"Requesting completion for the following formatted prompt: {context_prompt}.")

    print(st.session_state["messages"])

    msg = vertex_api.get_completion(user_question=prompt)

    st.session_state.messages.append({"author": "USER", "content": prompt})
    st.chat_message("USER").write(prompt)
    
    st.session_state.messages.append({"author": "AI", "content": msg})
    st.chat_message("AI").write(msg)