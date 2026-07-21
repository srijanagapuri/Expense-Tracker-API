from pydantic import BaseModel
from datetime import date

class Expense(BaseModel):
    title: str
    amount: float
    category: str
    expense_date: date
    description: str | None = None
    user_email: str
