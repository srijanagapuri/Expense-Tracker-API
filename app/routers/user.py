from fastapi import APIRouter, HTTPException
from app.database import db
from app.schemas.user import UserCreate
from app.utils.security import hash_password
from app.schemas.login import LoginRequest
from app.utils.security import verify_password
from app.auth import create_access_token
from fastapi import Depends
from app.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/register")
async def register(user: UserCreate):

    # Check if email already exists
    existing_user = await db.users.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user_data = user.model_dump()

    user_data["password"] = hash_password(user.password)

    await db.users.insert_one(user_data)

    return {
        "message": "User registered successfully"
    }

@router.post("/login")
async def login(login_data: LoginRequest):

    user = await db.users.find_one({"email": login_data.email})

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(login_data.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    access_token = create_access_token(
        data={"sub": user["email"]}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/profile")
async def get_profile(current_user=Depends(get_current_user)):
    return {
        "message": "Profile fetched successfully",
        "user": current_user
    }