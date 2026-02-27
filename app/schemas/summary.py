from typing import List
from pydantic import BaseModel


class SummaryRequest(BaseModel):
    feedbacks: List[str]