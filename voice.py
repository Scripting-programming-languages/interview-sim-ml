import whisper
import subprocess
import os
import numpy as np
from sentence_transformers import SentenceTransformer, util

AUDIO_FILE = "audio.mp3" # адрес изображение

FILLER_WORDS = ["эээ", "ну", "типа", "как бы", "короче", "значит"] # слова паразиты

PAUSE_THRESHOLD = 0.5  # дозволительная пауза в секундах

# загрузка модели
whisper_model = whisper.load_model("base")
semantic_model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

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
        word = w["word"].lower().strip()
        if word in FILLER_WORDS:
            fillers.append(word)
    return fillers

# удаление слов паразитов
def clean_text(text):
    for fw in FILLER_WORDS:
        text = text.replace(fw, "")
    return " ".join(text.split())


# расшифровка аудио
wav_file = "temp.wav"
convert_audio_to_wav(AUDIO_FILE, wav_file)

result = whisper_model.transcribe(wav_file, word_timestamps=True)
os.remove(wav_file)

raw_text = result["text"]

words = []
for seg in result["segments"]:
    if "words" in seg:
        words.extend(seg["words"])

pauses = detect_pauses(words)
fillers = count_fillers(words)
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
