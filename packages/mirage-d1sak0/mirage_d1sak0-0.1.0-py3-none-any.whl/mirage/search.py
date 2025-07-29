import requests
import sys
import time

DB_URL = "https://raw.githubusercontent.com/mogd-Kali/mirage/refs/heads/main/db.txt"

def _fetch_db_content(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке удаленного файла: {e}", file=sys.stderr)
        return None

def search_db(search_word: str):
    start_time = time.time()

    content = _fetch_db_content(DB_URL)

    if content is None:
        end_time = time.time()
        duration = end_time - start_time
        print(f"Время поиска : {duration:.2f} секунд.") # Выводим время даже при ошибке загрузки
        return []

    results = []
    search_word_lower = search_word.lower()
    for line in content.splitlines():
        if search_word_lower in line.lower():
            results.append(line)

    end_time = time.time()
    duration = end_time - start_time

    print("Все строки где нашол слово :")
    for line in results:
        print(line)

    print(f"Время поиска : {duration:.2f} секунд.")

    return results # Все еще возвращаем список найденных строк для гибкости