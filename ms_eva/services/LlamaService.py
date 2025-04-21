from langchain_community.llms import Ollama
from langchain_ollama import OllamaEmbeddings

def getLlamaLlmInstance():
    return Ollama(
        model = 'llama3.1',
        temperature = 0
    )

def getLlamaEmbeddingInstance():
    return OllamaEmbeddings(model="llama3.1")
