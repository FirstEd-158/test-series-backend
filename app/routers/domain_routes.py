from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.future import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models import Domain, DomainCreate, DomainUpdate
from app.database import get_session
from typing import List

router = APIRouter(prefix="/domains", tags=["Domains"])

@router.get("/", response_model=List[Domain])
async def get_domains(session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Domain))
    print(result)
    domains = result.scalars().all()
    print(domains)
    if not domains:
        raise HTTPException(status_code=404, detail="No domains added")
    return domains

@router.post("/add")
async def add_domain(domain_data: DomainCreate, session: AsyncSession = Depends(get_session)):
    domain = Domain(name=domain_data.name)
    session.add(domain)
    await session.commit()
    await session.refresh(domain)
    return domain

@router.get("/{domain_id}")
async def read_domain(domain_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Domain).where(Domain.id == domain_id))
    domain = result.scalar_one_or_none()
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    return domain

@router.put("/{domain_id}")
async def update_domain(domain_id: int, domain_data: DomainUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Domain).where(Domain.id == domain_id))
    domain = result.scalar_one_or_none()
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    for key, value in domain_data.dict().items():
        setattr(domain, key, value)
    session.add(domain)
    await session.commit()
    await session.refresh(domain)
    return domain

@router.delete("/{domain_id}")
async def delete_domain(domain_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.exec(select(Domain).where(Domain.id == domain_id))
    domain = result.scalar_one_or_none()
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found")
    await session.delete(domain)
    await session.commit()
    return {"msg": "Domain deleted", "id": domain_id}