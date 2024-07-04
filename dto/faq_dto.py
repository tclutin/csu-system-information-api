from typing import List, Optional

from pydantic import BaseModel


class CreateFAQDTO(BaseModel):
    question: str
    answer: str


class CreateFAQListDTO(BaseModel):
    faqs: List[CreateFAQDTO]


class SearchFAQDTO(BaseModel):
    message: str
    top_k: Optional[int] = 3
    min_similarity: Optional[float] = 0.7899
