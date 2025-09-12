from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import TestSeries, TestSeriesCreate
from app.database import get_session
from typing import List

router = APIRouter(prefix="/domains/{domain_id}/test_series", tags=["Domains", "Test Series"])

@router.get("/", response_model=List[TestSeries])
async def get_test_series(domain_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(TestSeries).where(TestSeries.domain_id == domain_id))
    test_series = result.scalars().all()
    if not test_series:
        raise HTTPException(status_code=404, detail="No test series added")
    return test_series

@router.post("/add")
async def add_test_series(domain_id: int, test_series_data: TestSeriesCreate, session: AsyncSession = Depends(get_session)):
    test_series = TestSeries(name=test_series_data.name, domain_id=domain_id)
    session.add(test_series)
    await session.commit()
    await session.refresh(test_series)
    return test_series

@router.get("/{test_series_id}")
async def read_test_series(test_series_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(TestSeries).where(TestSeries.id == test_series_id))
    test_series = result.scalar_one_or_none()
    if not test_series:
        raise HTTPException(status_code=404, detail="Test Series not found")
    return test_series

@router.put("/{test_series_id}")
async def update_test_series(test_series_id: int, test_series_data: TestSeries, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(TestSeries).where(TestSeries.id == test_series_id))
    test_series = result.scalar_one_or_none()
    if not test_series:
        raise HTTPException(status_code=404, detail="Test Series not found")
    for key, value in test_series_data.dict().items():
        setattr(test_series, key, value)
    session.add(test_series)
    await session.commit()
    await session.refresh(test_series)
    return test_series

@router.delete("/{test_series_id}")
async def delete_test_series(test_series_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(TestSeries).where(TestSeries.id == test_series_id))
    test_series = result.scalar_one_or_none()
    if not test_series:
        raise HTTPException(status_code=404, detail="Test Series not found")
    await session.delete(test_series)
    await session.commit()
    return {"msg": "Test Series deleted", "id": test_series_id}