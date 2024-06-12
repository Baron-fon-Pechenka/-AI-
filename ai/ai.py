from langchain.schema import HumanMessage, SystemMessage
from langchain.chat_models.gigachat import GigaChat

# Замените YOUR_API_KEY на ваш реальный ключ API
API_KEY = "NDIzNGZhMjgtYWMwNC00ODAwLTgxZDEtMGY4OTZmZGNmMzFjOmNjMmE3YTU1LTIyYWQtNDk4Ni05YWExLTM2ZGU2OTViYmYxNg=="
# NDIzNGZhMjgtYWMwNC00ODAwLTgxZDEtMGY4OTZmZGNmMzFjOmIzZDkzZDQ1LWVmZDItNDQ4Mi05N2E0LWM0YTMyNWRmNjJjMw==
# Создаем экземпляр клиента Gigachat
chat = GigaChat(credentials=API_KEY, verify_ssl_certs=False, scope="GIGACHAT_API_PERS")
def generate(content):
    messages = [
        SystemMessage(
            content=content)
    ]
    res = chat(messages)
    messages.append(res)
    return split_string(res.content)