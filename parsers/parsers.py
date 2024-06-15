import os
from bs4 import BeautifulSoup
import logging
import requests
import pandas as pd
import openpyxl

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


download_files(get_doc_links('/entrant/tselevoe-obuchenie/'), 'C:/Users/peper/PycharmProjects/-AI-/documents')
def extract_data_from_xlsx(file_path):
    """Извлекает все данные из xlsx-файла.
file_path = "-AI-/documents/1FPXFkpDPbfJwTOvmjWXGucnoEjrrmCEZsmd6T_kcpOo.xlsx"  # Замените на путь к вашему файлу
data = extract_data_from_xlsx(file_path)
print(data)
    """

    try:
        workbook = openpyxl.load_workbook(file_path)
        worksheet = workbook.active  # Используем активный лист по умолчанию

        data = []
        for row in worksheet.iter_rows(values_only=True):
            data.append(list(row))

        return data

    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None


def get_text(url):
    """
    Функция принимает URL-адрес, формирует полный URL, получает содержимое HTML-страницы
    и возвращает текстовые данные, найденные на этой странице.
    print(get_text("entrant/tselevoe-obuchenie/"))
    """
    base_url = "https://kubsau.ru/"
    full_url = base_url + url.lstrip("/")

    try:
        response = requests.get(full_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        page_content = soup.find('div', class_='page-content')
        if page_content:
            text = page_content.get_text(separator=' ', strip=True)
            return text
        else:
            return ""
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при получении данных: {e}")
        return []