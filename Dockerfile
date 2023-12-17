FROM python:3.11
EXPOSE 8080
WORKDIR /arxiv-chat
COPY . ./
RUN pip install -r requirements.txt
ENTRYPOINT ["streamlit", "run", "front.py", "--server.port=8080", "--server.address=0.0.0.0"]