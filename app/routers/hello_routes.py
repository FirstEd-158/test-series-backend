from fastapi import APIRouter, Depends
from app.deps import get_current_user

router = APIRouter(tags=["Hello"])

@router.get("/hello")
async def hello_world(user=Depends(get_current_user)):
    return {"msg": f"Hello, {user.username}!"}
