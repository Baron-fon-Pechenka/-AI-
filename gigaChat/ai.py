from langchain.schema import HumanMessage
from langchain.chat_models.gigachat import GigaChat
import os
from dotenv import load_dotenv
load_dotenv()
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from langchain.document_loaders import TextLoader

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
