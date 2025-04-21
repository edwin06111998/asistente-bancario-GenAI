import os
from openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
load_dotenv()

# API_KEY_OPENAI = os.environ['OPENAI_APIKEY']
API_KEY_OPENAI = "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"

def getOpenaiLlmInstance():
    return ChatOpenAI(
        api_key=API_KEY_OPENAI,
        model='gpt-4o-mini',
        temperature=0
    )

def getOpenaiEmbeddingInstance():
    return OpenAIEmbeddings(api_key = API_KEY_OPENAI)