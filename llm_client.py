from pprint import pprint
import requests
import time

# # LLM API
# API_KEY: str = "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6ImUzNDRlZjExLTQ0NzItNDFjMS1iOTA5LWQyMjlkMzZkN2Q0MCIsImV4cCI6NDkxNzM2MTUyOH0.a31bOPKDAjLEGmqCJtCEqOq8m4sEo35vrP7bVAN23pnzSi0UF8_jiS4AYfAT5lh9YrGflqvRMmVr27AwH-Yr1w"
# AI_MODEL: str = "mistralai/Mistral-Nemo-Instruct-2407"

# with open("lastnames.txt", "r", encoding="utf-8") as f:
#         lastnames = f.read()
# with open("termin_words.txt", "r", encoding="utf-8") as f:
#         termin_words = f.read()

api_key = "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6ImUzNDRlZjExLTQ0NzItNDFjMS1iOTA5LWQyMjlkMzZkN2Q0MCIsImV4cCI6NDkyNjM5MzMzOX0.mdQZRF3rIQ_quFh0aPuuDwxHK624QeX9fE7PwxaE-_F6-b_TB1JQBoJ53B_KiSAUVqDsXWAtiJ1JkrhQNXspnw"
ai_model = "mistralai/Mistral-Nemo-Instruct-2407"

BATCH_SIZE = 20
OUTPUT_FILE = "generated_queries_3.txt"


def make_request(message_text):
    url = "https://api.intelligence.io.solutions/api/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    data = {
        "model": ai_model,
        "messages": [
            {
                "role": "system",
                "content": "Ты эксперт по оценке устной речи студентов.",
            },
            {
                "role": "user",
                "content": message_text
            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    try:
        data = response.json()
    except Exception:
        return {"error": "invalid_json", "raw": response.text}

    if "choices" in data:
        return data["choices"][0]["message"]["content"]
    else:
        return data


def generate_queries(raw_text, cleaned_text, pauses, fillers):
    prompt = f"""
        Ты анализируешь устную речь студента.

        Исходный распознанный текст:
        {raw_text}

        Текст без слов-паразитов:
        {cleaned_text}

        Количество длинных пауз:
        {len(pauses)}

        Список пауз:
        {pauses}

        Количество слов-паразитов:
        {len(fillers)}

        Слова-паразиты:
        {fillers}

        Оцени качество речи.

        Дай ответ в формате дружелюбного совета:

        Общая оценка речи (1-10)
        Основные проблемы речи (пиши связным текстом, без перечислений, обращайся на вы)
        Что нужно улучшить (пиши связным текстом, без перечислений, обращайся на вы)
        """
    return make_request(prompt)



