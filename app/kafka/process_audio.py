from app.kafka.kafka_produces import send_to_kafka
from app.services.feedback import generate_feedback, generate_feedback_quality_of_speech
from app.services.semantic import final_score
from app.services.speech_quality import speech_quality_score
from app.services.voice import voice_transcription


def process_audio_task(audio, reference_text, answer_id):
    raw_text, cleaned_text, pauses, fillers, duration, clean_words = voice_transcription(audio)
    feedback2 = generate_feedback_quality_of_speech(raw_text, cleaned_text, pauses, fillers)
    score2 = speech_quality_score(clean_words, fillers, pauses, duration)

    feedback1 = generate_feedback(cleaned_text, reference_text, [])
    score1 = final_score(cleaned_text, reference_text, [])

    message = {
        "answer_id": answer_id,
        "score": score1,
        "speechScore": score2,
        "textFeedback": feedback1,
        "speechFeedback": feedback2,
        "transcribedText": cleaned_text
    }

    send_to_kafka("answerEstimation", message)