from fastapi import FastAPI
from app.routers.user import router as user_router
from app.routers.expense import router as expense_router

app = FastAPI(
    title="Expense Tracker API",
    version="1.0.0"
)

app.include_router(user_router)
app.include_router(expense_router)

@app.get("/")
def home():
    return {
        "message": "Expense Tracker API is running successfully!"
    }