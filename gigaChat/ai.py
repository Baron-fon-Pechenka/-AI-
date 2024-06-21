from langchain.schema import HumanMessage
from langchain_community.chat_models.gigachat import GigaChat
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.gigachat import GigaChatEmbeddings

load_dotenv()
API_KEY = os.getenv('API_SBERBANK_KEY')
chat = GigaChat(credentials=API_KEY, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")


def generate(content):
    messages = [
        HumanMessage(
            content=content)
    ]
    res = chat(messages)
    messages.append(res)
    return res.content


docs = db.similarity_search(input(), k=4)
