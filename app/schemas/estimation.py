from pydantic import BaseModel


class SingleAnswerEstimation(BaseModel):
    score: int
    speech_score: int
    text_feedback: str
    speech_feedback: str
    transcribed_text: str