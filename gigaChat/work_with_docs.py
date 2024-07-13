from dotenv import load_dotenv
import os
import pdfplumber
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.gigachat import GigaChatEmbeddings

load_dotenv()


def convert_pdf_to_txt(documents_dir):
    """
    Преобразует все PDF-файлы из указанной папки в TXT-файлы.

    Args:
        documents_dir (str): Путь к папке с документами.
    """
    # Перебираем все файлы в папке
    for filename in os.listdir(documents_dir):
        # Проверяем, является ли файл PDF-файлом
        if filename.endswith('.pdf'):
            # Формируем полный путь к PDF-файлу
            pdf_path = os.path.join(documents_dir, filename)

            # Открываем PDF-файл
            with pdfplumber.open(pdf_path) as pdf:
                # Извлекаем текст из всех страниц PDF
                text = ''
                for page in pdf.pages:
                    text += page.extract_text()

            # Формируем путь к TXT-файлу
            txt_filename = os.path.splitext(filename)[0] + '.txt'
            txt_path = os.path.join(documents_dir, txt_filename)

            # Сохраняем текст в TXT-файл
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write(text)

            print(f'PDF-файл "{filename}" успешно преобразован в TXT-файл "{txt_filename}"')


def files_to_embeddings():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    folder_path = os.path.join(current_dir, "documents", "pdf")
    db_path = os.path.join(current_dir, "documents", "chroma_db")
    loader = DirectoryLoader(folder_path, show_progress=True)
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
    )
    documents = text_splitter.split_documents(documents)
    embeddings = GigaChatEmbeddings(
        credentials=os.getenv('API_SBERBANK_KEY'), verify_ssl_certs=False
    )
    if os.listdir(db_path):
        db_chroma = Chroma(persist_directory=db_path, embedding_function=embeddings)
    else:
        db_chroma = Chroma.from_documents(
            documents,
            embeddings,
            persist_directory=db_path
        )
        db_chroma.persist()
    return db_chroma


db = files_to_embeddings()
