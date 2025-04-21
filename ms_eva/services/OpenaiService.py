import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

API_KEY_OPENAI = os.environ['OPENAI_APIKEY']

def getOpenaiLlmInstance():
    return ChatOpenAI(
        api_key=API_KEY_OPENAI,
        model='gpt-4o-mini',
        temperature=0
    )

def getOpenaiEmbeddingInstance():
    return OpenAIEmbeddings(api_key = API_KEY_OPENAI)