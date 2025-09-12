from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import Test, TestCreate
from app.database import get_session
from typing import List

router = APIRouter(prefix="/domains/{domain_id}/test_series/{test_series_id}/tests", tags=["Domains", "Test Series", "Tests"])

@router.get("/", response_model=List[Test])
async def get_tests(test_series_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Test).where(Test.test_series_id == test_series_id))
    test = result.scalars().all()
    if not test:
        raise HTTPException(status_code=404, detail="No tests added")
    return test

@router.post("/add")
async def add_test(test_series_id: int, test_data: TestCreate, session: AsyncSession = Depends(get_session)):
    test = Test(name=test_data.name, test_series_id=test_series_id, subject_id=test_data.subject_id)
    session.add(test)
    await session.commit()
    await session.refresh(test)
    return test

@router.get("/{test_id}")
async def read_test(test_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Test).where(Test.id == test_id))
    test = result.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    return test

@router.put("/{test_id}")
async def update_test(test_id: int, test_data: Test, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Test).where(Test.id == test_id))
    test = result.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    for key, value in test_data.dict().items():
        setattr(test, key, value)
    session.add(test)
    await session.commit()
    await session.refresh(test)
    return test

@router.delete("/{test_id}")
async def delete_test(test_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Test).where(Test.id == test_id))
    test = result.scalar_one_or_none()
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")
    await session.delete(test)
    await session.commit()
    return {"msg": "Test Series deleted", "id": test_id}