from datetime import date, datetime
from pydantic import BaseModel
from pydantic import ConfigDict


class GuideCreate(BaseModel):
    apuration_id: int
    guide_type: str
    due_date: date


class GuideResponse(BaseModel):
    id: int
    apuration_id: int
    guide_type: str
    amount: float
    due_date: date
    status: str

    model_config = ConfigDict(from_attributes=True)


class GuideOut(BaseModel):
    id: int
    apuration_id: int
    guide_type: str
    amount: float
    due_date: date
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class GuidePayRequest(BaseModel):
    paid_at: date