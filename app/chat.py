import streamlit as st
from arxivapi import ArxivAPI
from qdrantapi import QdrantAPI
from vertexapi import VertexAPI
from dotenv import load_dotenv
from prompts import context_prompt, standalone_question_prompt
import logging as log
import os

load_dotenv()

log.basicConfig(level=log.INFO, format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

# intialize vertex AI SDK and arxiv API
vertex_api = VertexAPI()
arxiv_api = ArxivAPI()
qdrant_client = QdrantAPI()

# with st.sidebar:
#     openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
#     "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
#     "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
#     "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 Chat over academic research papers.")
st.caption("🚀 I'm a chatbot that draws knwoledge from abstracts of papers published on arXiv in 2023 in the field of information retrieval (cs.IR).")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"author": "AI", "content": "Shoot a question!"}]

for msg in st.session_state.messages:
    st.chat_message(msg["author"]).write(msg["content"])

if prompt := st.chat_input():

    # get standalone question
    chat_history = [ f"{message['author']}: {message['content']}." for message in st.session_state["messages"]]
    chat_history = '\n'.join(chat_history)
    
    standalone_question_prompt = standalone_question_prompt.format(chat_history=chat_history, user_question=prompt)
    log.info(f"Standalone question prompt: {standalone_question_prompt}")

    standalone_question = vertex_api.get_standalone_question(standalone_question_prompt)
    log.info(f"Standalone questiont: {standalone_question}")


    # # RAG 
    # semantic search 
    hits = qdrant_client.query_index(collection_name='information_retrieval', query=prompt, k = 10)

    # format context
    context = []
    for hit in hits: 
        payload = hit.payload 
        context.append(f'Abstract: {payload["summary"]} - About the paper: {dict((k, payload[k]) for k in ("authors", "link", "published", "title"))}')

    context = '\n\n'.join(context)
    context_prompt = context_prompt.format(context=context)

    # get completion
    log.info(f"Requesting completion for the following formatted prompt: {context_prompt}.")

    msg = vertex_api.get_completion(context_prompt=context_prompt, user_question=standalone_question)

    st.session_state.messages.append({"author": "USER", "content": prompt})
    st.chat_message("USER").write(prompt)
    
    st.session_state.messages.append({"author": "AI", "content": msg})
    st.chat_message("AI").write(msg)