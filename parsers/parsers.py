import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(
    filename='../pdf_links.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def get_pdf_links(url):
    """
    Функция принимает URL-адрес, формирует полный URL, получает содержимое HTML-страницы
    и возвращает список ссылок на файлы PDF, найденные на этой странице.
    print(get_pdf_links("/entrant/tselevoe-obuchenie/"))
    """
    base_url = "https://kubsau.ru/"
    full_url = base_url + url.lstrip("/")

    try:
        response = requests.get(full_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, "html.parser")
        pdf_links = [base_url + link["href"] for link in soup.find_all("a", href=lambda href: href and "pdf" in href)]

        return pdf_links

    except requests.exceptions.RequestException as e:
        logging.error(f"Ошибка при получении данных: {e}")
        return []
