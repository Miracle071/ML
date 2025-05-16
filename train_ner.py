import json
import numpy as np
from datasets import Dataset
import evaluate
import transformers
import seqeval
import accelerate
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer

import transformers
print("Transformers version:", transformers.__version__)

import torch
print(torch.cuda.is_available())

# --- Загрузка и подготовка данных ---
with open("ner_bio_data.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# "raw_data" — список с элементами, где есть ключ "data" с предложениями
data = []
for entry in raw_data:
    data.extend(entry["data"])  # Собираем все предложения в один список

# Проверяем структуру
print(f"Всего предложений: {len(data)}")

# Формируем список всех меток
label_list = sorted(list({label for example in data for label in example["labels"]}))
label_to_id = {label: i for i, label in enumerate(label_list)}
id_to_label = {i: label for label, i in label_to_id.items()}

# --- Загружаем модель и токенизатор ---
model_name = "bert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=len(label_list))

# --- Функция токенизации и выравнивания меток ---
def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(
        examples["tokens"],
        is_split_into_words=True,
        truncation=True,
        padding="max_length",
        max_length=128,
    )
    labels = []
    word_ids = tokenized_inputs.word_ids(batch_index=0)
    previous_word_idx = None
    label_ids = []
    for word_idx in word_ids:
        if word_idx is None:
            label_ids.append(-100)
        elif word_idx != previous_word_idx:
            label_ids.append(label_to_id[examples["labels"][word_idx]])
        else:
            current_label = examples["labels"][word_idx]
            # Преобразуем B-метку во внутреннюю I-, если слово продолжается
            if current_label.startswith("B-"):
                current_label = "I-" + current_label[2:]
            label_ids.append(label_to_id.get(current_label, label_to_id["O"]))
        previous_word_idx = word_idx
    tokenized_inputs["labels"] = label_ids
    return tokenized_inputs

# Преобразуем в Dataset Hugging Face
dataset = Dataset.from_list(data)

# Применяем токенизацию с выравниванием
encoded_dataset = dataset.map(tokenize_and_align_labels)

# --- Загружаем метрику ---
metric = evaluate.load("seqeval")

# --- Функция подсчета метрик ---
def compute_metrics(p):
    predictions, labels = p
    predictions = np.argmax(predictions, axis=2)

    true_labels = [
        [id_to_label[l] for l in label if l != -100] for label in labels
    ]
    true_predictions = [
        [id_to_label[p] for (p, l) in zip(prediction, label) if l != -100]
        for prediction, label in zip(predictions, labels)
    ]

    results = metric.compute(predictions=true_predictions, references=true_labels)
    return {
        "precision": results["overall_precision"],
        "recall": results["overall_recall"],
        "f1": results["overall_f1"],
        "accuracy": results["overall_accuracy"],
    }

# --- Настройки обучения ---
print("TrainingArguments path:", transformers.TrainingArguments.__module__)

training_args = TrainingArguments(
    output_dir="./ner_model",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
)

# --- Создаем Trainer ---
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset,
    eval_dataset=encoded_dataset,  # Можно позже сделать разделение на train и val
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# --- Запускаем обучение ---
trainer.train()

# --- Сохраняем модель и токенизатор ---
import os
os.makedirs("./ner_model", exist_ok=True)

model.save_pretrained("./ner_model")
tokenizer.save_pretrained("./ner_model")

