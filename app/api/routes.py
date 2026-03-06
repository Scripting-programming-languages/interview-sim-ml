from fastapi import APIRouter, UploadFile, File, Form
from app.schemas.estimation import SingleAnswerEstimation
from app.schemas.report import FinalInterviewReport
from app.schemas.summary import SummaryRequest
from app.services.feedback import generate_feedback
from app.services.llm import ask_llm
from app.services.semantic import final_score

router = APIRouter()

@router.post("/estimate-answer", response_model=SingleAnswerEstimation)
async def estimate_answer(
    audio: UploadFile = File(...),
    reference_text: str = Form(...)
):
    # преобразование аудио в текст

    text = "Питон это язык программирования"
    feedback1 = generate_feedback(text, reference_text, [])
    score1 = final_score(text, reference_text, [])
    return SingleAnswerEstimation(
        score=score1,
        speech_score=0,
        text_feedback=feedback1,
        speech_feedback="",
        transcribed_text=text
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