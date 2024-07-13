import os
from bs4 import BeautifulSoup
import logging
import requests
import pandas as pd
import openpyxl
from tqdm import tqdm
from threading import Thread
from tqdm import tqdm

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
    base_url = "https://kubsau.ru"
    full_url = base_url + url

    try:
        response = requests.get(full_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")

        pdf_links = []
        for link in soup.find_all("a", href=lambda href: href and "pdf" in href):
            pdf_link = base_url + link["href"]
            pdf_links.append(pdf_link)
        for i,link in enumerate(pdf_links):
            if link.count('https://kubsau.ru/')==0:
                pdf_links[i] = pdf_links[i].replace('https://kubsau.ru',full_url, 1)
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

    def __init__(self, file_name="Неизвестно", error_message=None):
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


def download_file(url, file_path):
    try:
        response = requests.get(url)
        response.raise_for_status()

        with open(file_path, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при скачивании файла {file_path}: {e}")
        raise DownloadError(file_path, str(e))
def create_file_name(folder_path):
    """
    Создает название файла на основе количества файлов в папке.

    Args:
        folder_path (str): Путь к папке, в которой будут создаваться файлы.

    Returns:
        str: Название файла в формате "pdf_документ_НОМЕР.pdf".
    """
    # Получаем список файлов в папке
    file_list = os.listdir(folder_path)

    # Считаем количество файлов
    file_count = len(file_list)

    # Формируем название файла
    file_name = f"pdf_документ_{file_count + 1}.pdf"

    return file_name
def download_files(links, download_dir):
    '''
    Скачивает PDF-файлы и Google Таблицы из списка ссылок в указанную папку.

    Args:
        links (list): список ссылок на PDF-файлы и Google Таблицы
        download_dir (str): путь к папке, куда будут сохранены файлы
    '''
    os.makedirs(download_dir, exist_ok=True)

    # Перебираем список ссылок
    for link in links:
        if 'pdf' in link:
            while not link.endswith('pdf'):
                link = link[:-1]
            # Получаем имя файла из ссылки
            file_name = create_file_name(download_dir)
            file_path = f"{download_dir}\\{file_name}"

            # Скачиваем PDF-файл
            try:
                t = Thread(target=download_file, args=(link, file_path))
                t.start()
                with tqdm(total=100, unit='%', desc=f"Скачивание {file_name}", leave=False) as pbar:
                    while t.is_alive():
                        pbar.update(1)
            except DownloadError as e:
                logging.error(f"Ошибка при скачивании файла {e.file_name}: {e.message}")
                raise e

        elif 'spreadsheets' in link:
            file_name = link.split('/')[-2] + '.xlsx'
            try:
                link = link[:link.rfind('/')] + "/export?format=xlsx"
                file_path = f"{download_dir.replace('pdf','xlsx')}/{file_name}"
                t = Thread(target=download_file, args=(link, file_path))
                t.start()
                with tqdm(total=100, unit='%', desc=f"Скачивание {file_name}", leave=False) as pbar:
                    while t.is_alive():
                        pbar.update(1)
            except DownloadError as e:
                logging.error(f"Ошибка при скачивании Google таблицы: {e.message}")
                raise e
        else:
            logging.error(f"Неподдерживаемый тип ссылки: {link}")
            raise DownloadError(link, "Неподдерживаемый тип ссылки")


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

def parse_all():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_dir = os.path.join(current_dir, "gigaChat", "documents", "pdf").replace('parsers\\', '')
    paths = [
        "entrant/invalid/",
        "entrant/",
        "entrant/docs/bakalavriat-spetsialitet-magistratura/",
        "entrant/ways/",
        "entrant/courses/",
        "entrant/tselevoe-obuchenie/",
        "entrant/podig/obshchezhitiya/",
        "education/military/anonce/",
        "education/military/doc/"
    ]

    with tqdm(total=len(paths), desc='Parsing paths') as pbar:
        for path in paths:
            get_text(path)
            download_files(get_doc_links('/' + path), os.path.join(os.getcwd(), pdf_dir))
            pbar.update(1)
        print('-' * 100, '\nВсе файлы скачаны!\n', '-' * 100)

def run():
    parse_all()