from flask import Flask, render_template, request, jsonify
from parsing.crawler import parse_products
from parsing.prouct_ner import extract_products_ner

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/extract', methods=['POST'])
def api_extract():
    url = request.json.get('url')
    raw_products = parse_products(url)  # Парсинг
    products = extract_products_ner(raw_products)  # Извлечение сущностей
    return jsonify({"products": products})

if __name__ == '__main__':
    app.run(debug=True)