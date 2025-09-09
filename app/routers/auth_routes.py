from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import User
from app.auth import hash_password, verify_password, create_access_token
from app.database import get_session

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
async def register_user(username: str, password: str, session: AsyncSession = Depends(get_session)):
    user_exists = await session.execute(select(User).where(User.username == username))
    if user_exists.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Username already exists")
    
    user = User(username=username, hashed_password=hash_password(password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return {"msg": "User registered", "id": user.id}

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
