from app.kafka.kafka_produces import send_to_kafka
from app.services.feedback import generate_feedback, generate_feedback_quality_of_speech
from app.services.semantic import final_score
from app.services.speech_quality import speech_quality_score
from app.services.voice import voice_transcription


def process_audio_task(audio_bytes, reference_text, answer_id):
    #raw_text, cleaned_text, pauses, fillers, duration, clean_words = voice_transcription(audio_bytes)
    #feedback2 = generate_feedback_quality_of_speech(raw_text, cleaned_text, pauses, fillers)
    #score2 = speech_quality_score(clean_words, fillers, pauses, duration)
    cleaned_text = "Python это язык программирования"
    feedback1 = generate_feedback(cleaned_text, reference_text, [])
    score1 = final_score(cleaned_text, reference_text, [])

    message = {
        "answer_id": answer_id,
        "score": score1,
        "speech_score": 0, #score2,
        "text_feedback": feedback1,
        "speech_feedback": "ok", #feedback2,
        "transcribed_text": cleaned_text
    }

    send_to_kafka("answerEstimation", message)