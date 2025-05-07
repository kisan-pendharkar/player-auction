from pydantic import BaseModel
from typing import List

class PaginatedResponse(BaseModel):
    success: bool
    message: str
    data: List[dict]
    total: int
    limit: int
    offset: int