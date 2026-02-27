
from pydantic import BaseModel


class FinalInterviewReport(BaseModel):
    summary_feedback: str