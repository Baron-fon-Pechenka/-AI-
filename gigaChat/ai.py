from langchain.schema import SystemMessage
from langchain.schema import BaseMessage
from langchain.schema import HumanMessage
from langchain_community.chat_models.gigachat import GigaChat
import os
from dotenv import load_dotenv
from .work_with_docs import db

load_dotenv()
API_KEY = os.getenv('API_SBERBANK_KEY')
chat = GigaChat(credentials=API_KEY, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")

def check_answer(query, text_to_check):
    print(query[:-54])
    system_message = SystemMessage(
        content=f"""
            Вопрос :"{query[:-54]}".
            Ответ: {text_to_check}.
            
            1) Является ли ответ на вопрос адекватным? (да/нет).
            2) Является ли вопрос прямо и чётко относящимся к обучению или поступлению в учебное заведение? (да/нет).
            На выходе выдай односложно "да" , если на оба вопроса ты ответил "да", в противном случае выдай "нет".
            """
    )
    messages = [system_message]
    res = chat(messages)
    messages.append(res)
    return res.content
def reformat_text(text_to_format, query):
    system_message = SystemMessage(
        content=f"""
            Вы получили запрос, состоящий из условия и текстовых данных. 
            Ваша задача - привести текстовую информацию к красивому формату, 
            не удаляя и не добавляя информацию.
            Ваш ответ должен быть структурирован и оформлен максимально удобочитаемым образом. 
            Возможно использование маркированных списков, заголовков, разделителей и 
            других форматирующих элементов.
            Пожалуйста, обратите внимание, что вам запрещено изменять, добавлять или 
            удалять какую-либо информацию из изначального запроса. 
            Вы должны только отформатировать ее должным образом.
            Я рассчитываю на ваше понимание инструкций и надеюсь, что вы 
            предоставите мне ответ в желаемом формате.
            Условие: {query}
            """
    )
    messages = [system_message, HumanMessage(content=text_to_format)]
    res = chat(messages)
    messages.append(res)
    return res.content


def find_in_files(query: str):
    docs = db.similarity_search(query , k=6)
    file_paths = []
    text = ''
    if len(docs) > 0:
        for ind, doc in enumerate(docs):
            file_paths.append(doc.metadata['source'].replace('txt/', '').replace('.txt', '.pdf'))
            text += f"{ind + 1})\n {doc.page_content}\n{'-' * 8}"
        return text, set(file_paths)

    else:
        print(text,file_paths)
        return ('Увы, я не знаю этого, возможно, вы задали вопрос не о поступлении в КУБГАУ, либо в '
                'предоставленной мне моими создателя документации нет такой информации :('), None
