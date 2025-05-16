import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from transformers import AutoTokenizer, AutoModelForTokenClassification
from transformers import pipeline

app = FastAPI()

# Загружаем модель и токенизатор (замени на путь к своей модели)
model_name_or_path = "./ner_model"  # Папка с обученной моделью
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
model = AutoModelForTokenClassification.from_pretrained(model_name_or_path)

# Создаём пайплайн для NER
nlp = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

class URLItem(BaseModel):
    url: str

@app.post("/extract-products")
def extract_products(item: URLItem):
    try:
        resp = requests.get(item.url, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {e}")

    # Парсим HTML и извлекаем текст
    soup = BeautifulSoup(resp.text, "html.parser")
    texts = soup.stripped_strings
    full_text = " ".join(texts)

    # Прогоняем текст через NER пайплайн
    ner_results = nlp(full_text)

    # Фильтруем только сущности мебели (предположим, у тебя метка FURN)
    furn_entities = [ent["word"] for ent in ner_results if "FURN" in ent["entity_group"]]

    # Уникальные названия мебели
    furn_entities = list(set(furn_entities))

    return {"products": furn_entities}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
