from langchain.schema import HumanMessage
from langchain.chat_models.gigachat import GigaChat
from dotenv import load_dotenv
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
)
from langchain.document_loaders import TextLoader
import pdfplumber
import os
import pdfplumber


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


# Вызываем функцию для преобразования PDF-файлов в TXT-файлы
convert_pdf_to_txt('../documents')
