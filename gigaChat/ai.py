from langchain.schema import HumanMessage
from langchain.chat_models.gigachat import GigaChat

API_KEY = "NDIzNGZhMjgtYWMwNC00ODAwLTgxZDEtMGY4OTZmZGNmMzFjOmNjMmE3YTU1LTIyYWQtNDk4Ni05YWExLTM2ZGU2OTViYmYxNg=="
chat = GigaChat(credentials=API_KEY, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")


def generate(content):
    messages = [
        HumanMessage(
            content=content)
    ]
    res = chat(messages)
    messages.append(res)
    return res.content
