import os
from bs4 import BeautifulSoup
import logging
import requests
import pandas as pd

logging.basicConfig(
    filename='../download_files.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def get_doc_links(url):
    """
    Функция принимает URL-адрес, формирует полный URL, получает содержимое HTML-страницы
    и возвращает список ссылок на файлы PDF и Google Таблицы, найденные на этой странице.
    """
    base_url = "https://kubsau.ru/"
    full_url = base_url + url.lstrip("/")

    try:
        response = requests.get(full_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        pdf_links = [base_url + link["href"] for link in soup.find_all("a", href=lambda href: href and "pdf" in href)]
        google_sheet_links = [link["href"] for link in
                              soup.find_all("a", href=lambda href: href and "docs.google.com/spreadsheets" in href)]

        return pdf_links + google_sheet_links

    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при получении данных: {e}")
        return []


class DownloadError(Exception):
    """
    Исключение, возникающее при ошибках при скачивании файлов.

    Attributes:
        file_name (str): Имя файла, при скачивании которого возникла ошибка.
        error_message (str): Текст ошибки, описывающий причину ошибки.
    """

    def __init__(self, file_name, error_message):
        """
        Инициализирует объект DownloadError.

        Args:
            file_name (str): Имя файла, при скачивании которого возникла ошибка.
            error_message (str): Текст ошибки, описывающий причину ошибки.
        """
        self.file_name = file_name
        self.error_message = error_message

    def __str__(self):
        """
        Возвращает строковое представление объекта DownloadError.

        Returns:
            str: Строковое представление объекта DownloadError.
        """
        return f"Ошибка при скачивании файла {self.file_name}: {self.error_message}"


def download_files(links, download_dir):
    '''
    Скачивает PDF-файлы и Google Таблицы из списка ссылок в указанную папку.

    Args:
        links (list): список ссылок на PDF-файлы и Google Таблицы
        download_dir (str): путь к папке, куда будут сохранены файлы
    '''
    # Создаем папку, если она не существует
    os.makedirs(download_dir, exist_ok=True)

    # Перебираем список ссылок
    for link in links:
        if 'pdf' in link:
            while not link.endswith('pdf'):
                link = link[:-1]
            # Получаем имя файла из ссылки
            file_name = os.path.basename(link)
            file_path = f"{download_dir}/{file_name}"

            # Скачиваем PDF-файл
            try:
                response = requests.get(link)
                response.raise_for_status()

                with open(file_path, 'wb') as file:
                    file.write(response.content)

            except requests.exceptions.RequestException as e:
                logging.error(f"Ошибка при скачивании файла {file_name}: {e}")
                raise DownloadError(f"Ошибка при скачивании файла {file_name}: {e}")

        elif 'spreadsheets' in link:
            try:
                file_name = link.split('/')[-2] + '.xlsx'
                link = link[:link.rfind('/')] + "/export?format=xlsx"
                file_path = f"{download_dir}/{file_name}"
                df = pd.read_excel(link)
                df.to_excel(file_path, index=False)
                print(f"Скачана Google Таблица {file_name}")
            except Exception as e:
                logging.error(f"Ошибка при скачивании Google Таблицы {file_name}: {e}")
                raise DownloadError(file_name, str(e))
        else:
            logging.error(f"Неподдерживаемый тип ссылки: {link}")
            raise DownloadError(link, "Неподдерживаемый тип ссылки")


download_files(get_doc_links('/entrant/tselevoe-obuchenie/'), 'C:/Users/Дмитрий/Desktop/-AI-/documents')
