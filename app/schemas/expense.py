from pydantic import BaseModel, Field
from datetime import date

class ExpenseCreate(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    amount: float = Field(..., gt=0)
    category: str
    expense_date: date
    description: str | None = None