import os
import redis
import json
from langchain_redis import RedisVectorStore
from langchain_redis import RedisChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain.docstore.document import Document
from ms_eva.services.UtilService import *
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ms_eva.services.OpenaiService import getOpenaiEmbeddingInstance
# from ms_eva.services.LlamaService import getLlamaEmbeddingInstance

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
r = redis.Redis(host='localhost', port=6379, db=0)
embeddings = getOpenaiEmbeddingInstance()
# embeddings = getLlamaEmbeddingInstance()

vector_store = RedisVectorStore(embeddings, redis_url=REDIS_URL, index_name="eva_docs")

def index_text_as_embeddings(text: str, source: str):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )
    chunks = splitter.split_text(text)
    documents = [
        Document(page_content=chunk, metadata={"source": source})
        for chunk in chunks
    ]
    vector_store.add_documents(documents)

def query_vector_store(query):
    retriever = vector_store.as_retriever()
    results = retriever.invoke(query)
    response = None if results is None else results
    return response

def get_redis_history(session_id: str):
    response = RedisChatMessageHistory(session_id, redis_url=REDIS_URL, key_prefix='eva_', ttl=3600)
    return response

def save_redis_history(userMessage: str, assistantMessage: str, userId: str):
    message_history = get_redis_history(userId)
    message_history.add_message(HumanMessage(content=userMessage))
    message_history.add_message(AIMessage(content=assistantMessage))

def clear_redis_history(session_id: str):
    history = get_redis_history(session_id)
    history.clear()

def save_state(session_id: str, state: dict):
    r.set(f"state:{session_id}", json.dumps(state))

def load_state(session_id: str) -> dict:
    raw = r.get(f"state:{session_id}")
    return json.loads(raw) if raw else {}

def clear_state(session_id: str):
    r.delete(f"state:{session_id}")

def loadEmbedding():
    r.flushdb()
    index_text_as_embeddings(infoVectorBG, source="https://www.bancoguayaquil.com/")

retriever = vector_store.as_retriever()