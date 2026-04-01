import subprocess
import string
from faster_whisper import WhisperModel
import tempfile

AUDIO_FILE = "audio.mp3"                                           # адрес изображение
FILLER_WORDS = ["ну", "вот", "как", "типа", "значит", "короче",    # слова паразиты
                "вообще", "собственно", "скажем", "допустим", 
                "например", "так", "это", "блин", "понимаешь", 
                "понимаете", "знаешь", "знаете", "смотри", 
                "слушай"] 
PAUSE_THRESHOLD = 0.5                                              # дозволительная пауза в секундах

# загрузка модели
model = WhisperModel("small", device="cpu", compute_type="int8")

# преобразование к формату .wav
def convert_audio_to_wav(audio_bytes):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as input_tmp:
        input_tmp.write(audio_bytes)
        input_path = input_tmp.name
    output_path = ""
    base_of_postfixes = [".mp3", ".webm", ".ogg"]
    for postfix in base_of_postfixes:
        output_path = input_path.replace(postfix, ".wav")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", input_path,
        "-ar", "16000",
        "-ac", "1",
        output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

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
def voice_transcription(file):
    wav_file = convert_audio_to_wav(file)

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
    duration = words[-1]["end"] if words else 0
    
    return raw_text, cleaned_text, pauses, fillers, duration, clean_words 

