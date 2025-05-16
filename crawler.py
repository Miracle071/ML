import pandas as pd
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

def load_links_from_csv(file_path):
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
        links = df.iloc[:, 0].dropna().astype(str).tolist()
        print(f"[INFO] Загружено {len(links)} ссылок из файла.")
        return links
    except Exception as e:
        print(f"[ERROR] Не удалось загрузить CSV: {e}")
        return []

def is_working_link(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

def get_visible_text_from_url(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        return "\n".join(line.strip() for line in text.splitlines() if line.strip())
    except Exception as e:
        print(f"[ERROR] Ошибка при парсинге {url}: {e}")
        return None

def save_text_to_file(text, index, output_folder="pages_text"):
    os.makedirs(output_folder, exist_ok=True)
    file_path = os.path.join(output_folder, f"page_{index+1}.txt")
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"[SAVED] page_{index+1}.txt")
    except Exception as e:
        print(f"[ERROR] Не удалось сохранить файл {file_path}: {e}")

def main(csv_path):
    links = load_links_from_csv(csv_path)
    if not links:
        print("[STOP] Ссылки не загружены. Проверь CSV.")
        return

    working_links = []

    print("[INFO] Проверка ссылок на доступность...")
    for url in links:
        if len(working_links) >= 100:
            break
        print(f"→ Проверка: {url}")
        if is_working_link(url):
            print(f"✅ Работает: {url}")
            working_links.append(url)
        else:
            print(f"❌ Не доступна: {url}")

    print(f"[RESULT] Найдено {len(working_links)} рабочих ссылок.")

    print("[INFO] Парсинг текста с рабочих страниц...")
    for i, url in enumerate(working_links):
        print(f"→ Обработка {i+1}/100: {url}")
        text = get_visible_text_from_url(url)
        if text:
            save_text_to_file(text, i)
        else:
            print(f"[WARN] Текст не получен: {url}")

if __name__ == "__main__":
    # Укажи здесь путь к твоему CSV-файлу
    main("URL_list.csv")
