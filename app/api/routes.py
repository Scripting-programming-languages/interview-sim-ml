from fastapi import APIRouter, UploadFile, File, Form
from app.schemas.estimation import SingleAnswerEstimation
from app.schemas.report import FinalInterviewReport
from app.schemas.summary import SummaryRequest

router = APIRouter()

@router.post("/estimate-answer", response_model=SingleAnswerEstimation)
async def estimate_answer(
    audio: UploadFile = File(...),
    reference_text: str = Form(...)
):
    pass


@router.post("/finalize-feedback", response_model=FinalInterviewReport)
async def finalize_feedback(request: SummaryRequest):
    pass