from fastapi import APIRouter, UploadFile, File, Form
from app.schemas.estimation import SingleAnswerEstimation
from app.schemas.report import FinalInterviewReport
from app.schemas.summary import SummaryRequest
from app.services.feedback import generate_feedback, generate_feedback_quality_of_speech
from app.services.llm import ask_llm
from app.services.semantic import final_score
from app.services.voice import voice_transcription
from app.services.speech_quality import speech_quality_score

router = APIRouter()

@router.post("/estimate-answer", response_model=SingleAnswerEstimation)
async def estimate_answer(
    audio: UploadFile = File(...),
    reference_text: str = Form(...)
):
    # преобразование аудио в текст
    raw_text, cleaned_text, pauses, fillers, duration, clean_words = voice_transcription(audio)
    feedback2 = generate_feedback_quality_of_speech(raw_text, cleaned_text, pauses, fillers)
    score2 = speech_quality_score(clean_words, fillers, pauses, duration)

    # text = "Питон это язык программирования"
    feedback1 = generate_feedback(cleaned_text, reference_text, [])
    score1 = final_score(cleaned_text, reference_text, [])
    return SingleAnswerEstimation(
        score=score1,
        speech_score=score2,
        text_feedback=feedback1,
        speech_feedback=feedback2,
        transcribed_text=cleaned_text
    )


@router.post("/finalize-feedback", response_model=FinalInterviewReport)
async def finalize_feedback(request: SummaryRequest):
    query = ''' Сделай саммари из этих фидбеков. Короткое и ТОЛЬКО на РУССКОМ языке.
    Выдели самое главное. Не хвали без причины и не фанатзируй. Тексты фидбеков ниже:

    '''
    text = "\n".join(request.feedbacks)
    query += text
    summary = ask_llm(query)
    return FinalInterviewReport(
        summary_feedback=summary
    )