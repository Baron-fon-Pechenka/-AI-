from langchain.schema import HumanMessage
from langchain_community.chat_models.gigachat import GigaChat
import os
from dotenv import load_dotenv
from work_with_docs import db

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

docs = db.similarity_search('какие нужны документы иностранцу для поступления', k=4)
for doc in docs:
    print('-'*100)
    for item in doc:
        print(item)