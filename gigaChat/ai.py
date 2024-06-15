from langchain.schema import HumanMessage
from langchain_community.chat_models.gigachat import GigaChat
import os
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
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


# Получаем текущую директорию, в которой находится исполняемый файл
current_dir = os.path.dirname(os.path.abspath(__file__))

# Переходим на уровень выше и заходим в папку "documents"
documents_dir = os.path.join(current_dir, "documents").replace('\\gigaChat', '').replace('\\', '/')

# Находим все txt файлы в папке "documents"
txt_files = [f for f in os.listdir(documents_dir) if f.endswith(".txt")]

for txt_file in txt_files:
    txt_file_path = f"{documents_dir}/{txt_file}"
    loader = TextLoader(txt_file_path, encoding='utf-8')
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    documents = text_splitter.split_documents(documents)
    print(f"Total documents: {len(documents)}")
embeddings = GigaChatEmbeddings(
    credentials=API_KEY, verify_ssl_certs=False
)
db = Chroma.from_documents(
    documents,
    embeddings,
    client_settings=Settings(anonymized_telemetry=False),
)
docs = db.similarity_search(input(), k=4)
print(len(docs))