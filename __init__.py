import os
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
# from parsers import parsers
# parsers.run()
from bot import front

front.run()
