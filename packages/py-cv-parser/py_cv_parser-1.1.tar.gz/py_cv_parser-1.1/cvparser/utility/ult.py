from langdetect import detect
import os
import re
def filetype_detect(file:str)->str:
    filetype = file.split('.')[-1]
    return filetype


def language_detect(language:str):
    language = detect(language)
    return language


def get_filename(file:str):
    dotindex=file.rfind('.')
    if file.rfind('/')!= -1:
        slashindex = file.rfind('/')
    else:
        slashindex = file.rfind('\\')


    return file[slashindex+1:dotindex]

def get_filesize(file:str):
    file_size = os.path.getsize(file)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if file_size < 1024.0:
            return f"{file_size:.2f} {unit}"
        file_size /= 1024.0


def clean_text(text):

    text = re.sub(r"\f+", "\n", text)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text

def count_words(text:str):
    count = len(text.split())
    return count