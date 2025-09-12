from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import Subject, SubjectCreate
from app.database import get_session
from typing import List

router = APIRouter(prefix="/domains/{domain_id}/subjects", tags=["Domains"])

@router.get("/", response_model=List[Subject])
async def get_subjects(domain_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Subject).where(Subject.domain_id == domain_id))
    subjects = result.scalars().all()
    if not subjects:
        raise HTTPException(status_code=404, detail="No subjects added")
    return subjects

@router.post("/add")
async def add_subject(domain_id: int, subject_data: SubjectCreate, session: AsyncSession = Depends(get_session)):
    subject = Subject(name=subject_data.name, domain_id=domain_id)
    session.add(subject)
    await session.commit()
    await session.refresh(subject)
    return subject

@router.get("/{subject_id}")
async def read_subject(subject_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Subject).where(Subject.id == subject_id))
    subject = result.scalar_one_or_none()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

@router.put("/{subject_id}")
async def update_subject(subject_id: int, subject_data: Subject, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Subject).where(Subject.id == subject_id))
    subject = result.scalar_one_or_none()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    for key, value in subject_data.dict().items():
        setattr(subject, key, value)
    session.add(subject)
    await session.commit()
    await session.refresh(subject)
    return subject

@router.delete("/{subject_id}")
async def delete_subject(subject_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Subject).where(Subject.id == subject_id))
    subject = result.scalar_one_or_none()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    await session.delete(subject)
    await session.commit()
    return {"msg": "Subject deleted", "id": subject_id}