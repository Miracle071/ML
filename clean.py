import re
import json
import os

# Список ключевых мебельных слов
furniture_keywords = [
    "mattress", "sofa", "couch", "chair", "table", "bed", "wardrobe", "dresser", "desk",
    "bench", "ottoman", "cabinet", "bookshelf", "nightstand", "stool", "chest of drawers"
]

# Сортируем по длине, чтобы сначала искать длинные
furniture_keywords_sorted = sorted(furniture_keywords, key=len, reverse=True)
keywords_pattern = r"|".join(map(re.escape, furniture_keywords_sorted))

# Регулярное выражение для захвата названий мебели с деталями
pattern = re.compile(
    rf"([A-Z0-9a-z\s,]*?\b(?:{keywords_pattern})\b[\w\s\-\,]*)",
    re.IGNORECASE
)

# Папка с .txt файлами (в каждой строке — описание/название товара)
input_folder = "pages_text"
output_file = "extracted_furniture_names.json"

results = []

# Проходим по всем файлам .txt в папке
for filename in sorted(os.listdir(input_folder)):
    if filename.endswith(".txt"):
        filepath = os.path.join(input_folder, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            lines = f.readlines()

        extracted_names = []
        for line in lines:
            matches = pattern.findall(line)
            for match in matches:
                clean_name = match.strip(" ,-\n")
                if clean_name:  # если не пустое
                    extracted_names.append(clean_name)

        results.append({
            "filename": filename,
            "furniture_names": extracted_names
        })

# Сохраняем результаты в JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"Готово! Названия мебели сохранены в {output_file}")
