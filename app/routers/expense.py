from fastapi import APIRouter, Depends
from app.database import db
from app.schemas.expense import ExpenseCreate
from app.dependencies import get_current_user
from bson import ObjectId
from fastapi import HTTPException

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"]
)


@router.post("/")
async def create_expense(
    expense: ExpenseCreate,
    current_user=Depends(get_current_user)
):
    expense_data = expense.model_dump()

    # Link the expense to the logged-in user
    expense_data["user_email"] = current_user["email"]

    result = await db.expenses.insert_one(expense_data)

    return {
        "message": "Expense added successfully",
        "expense_id": str(result.inserted_id)
    }


@router.get("/")
async def get_expenses(current_user=Depends(get_current_user)):

    expenses = []

    async for expense in db.expenses.find(
        {"user_email": current_user["email"]}
    ):
        expense["_id"] = str(expense["_id"])
        expenses.append(expense)

    return expenses



@router.get("/{expense_id}")
async def get_expense(
    expense_id: str,
    current_user=Depends(get_current_user)
):

    expense = await db.expenses.find_one(
        {
            "_id": ObjectId(expense_id),
            "user_email": current_user["email"]
        }
    )

    if not expense:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    expense["_id"] = str(expense["_id"])

    return expense

@router.put("/{expense_id}")
async def update_expense(
    expense_id: str,
    expense: ExpenseCreate,
    current_user=Depends(get_current_user)
):
    
    update_data = expense.model_dump()
    update_data["user_email"] = current_user["email"]

    result = await db.expenses.update_one(
        {
            "_id": ObjectId(expense_id),
            "user_email": current_user["email"]
        },
        {
            "$set": update_data
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense updated successfully"
    }

@router.delete("/{expense_id}")
async def delete_expense(
    expense_id: str,
    current_user=Depends(get_current_user)
):

    result = await db.expenses.delete_one(
        {
            "_id": ObjectId(expense_id),
            "user_email": current_user["email"]
        }
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "message": "Expense deleted successfully"
    }