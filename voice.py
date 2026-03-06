# import whisper
import subprocess
import os
import numpy as np
from sentence_transformers import SentenceTransformer, util
import string
from faster_whisper import WhisperModel
from llm_client import generate_queries

AUDIO_FILE = "audio.mp3" # адрес изображение

FILLER_WORDS = ["вот", "ну", "типа", "как бы", "короче", "значит"] # слова паразиты

PAUSE_THRESHOLD = 0.5  # дозволительная пауза в секундах

# загрузка модели
# whisper_model = whisper.load_model("base")
# semantic_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
model = WhisperModel("small", device="cpu", compute_type="int8")


# преобразование к формату .wav
def convert_audio_to_wav(input_path, output_path):
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# определение больших пауз
def detect_pauses(words):
    pauses = []
    for i in range(len(words) - 1):
        gap = words[i + 1]["start"] - words[i]["end"]
        if gap > PAUSE_THRESHOLD:
            pauses.append(round(gap, 2))
    return pauses

# определение слов паразитов
def count_fillers(words):
    fillers = []
    for w in words:
        if w.lower() in FILLER_WORDS:
            fillers.append(w)
    return fillers

# удаление слов паразитов
def clean_text(raw_text):
    words = raw_text.split(" ")
    cleaned = ""
    for w in words:
        word = w.strip(string.whitespace + string.punctuation).lower()
        if word not in FILLER_WORDS:
            cleaned += w + " "
    return cleaned


# расшифровка аудио
wav_file = "temp.wav"
convert_audio_to_wav(AUDIO_FILE, wav_file)

segments, info = model.transcribe(
    wav_file,
    word_timestamps=True,
    language=None  
)

raw_text = ""

words = []

for segment in segments:
    raw_text += segment.text + " "
    if segment.words:
        for w in segment.words:
            words.append({
                "word": w.word,
                "start": w.start,
                "end": w.end
            })

word_list = [w["word"] for w in words]
clean_words = [w.strip(string.whitespace + string.punctuation) for w in word_list]

pauses = detect_pauses(words)
fillers = count_fillers(clean_words)
cleaned_text = clean_text(raw_text)

# результаты 
print("Распознанный текст:")
print(raw_text)

print("\nОчищенный текст:")
print(cleaned_text)

print("\nПаузы:")
print(f"Количество: {len(pauses)}")
if pauses:
    print(f"Все паузы: {pauses}")

print("\nСлова-паразиты:")
print(f"Количество: {len(fillers)}")
print(f"Список: {fillers}")

feedback = generate_queries(
    raw_text,
    cleaned_text,
    pauses,
    fillers
)

print(feedback)
