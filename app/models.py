from sqlmodel import SQLModel, Field
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column
from typing import Optional, Dict
from datetime import datetime, timezone

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True, nullable=False)
    hashed_password: str
class UserCreate(SQLModel):
    username: str
    password: str

class Domain(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(index=True)
class DomainCreate(SQLModel):
    name: str
class DomainUpdate(SQLModel):
    name: str

class Subject(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(index=True)
    domain_id: int = Field(foreign_key="domain.id", index=True)
class SubjectCreate(SQLModel):
    name: str

class TestSeries(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(index=True)
    domain_id: int = Field(foreign_key="domain.id", index=True)
class TestSeriesCreate(SQLModel):
    name:str

class Test(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    name: str = Field(index=True)
    test_series_id: int = Field(foreign_key="testseries.id", index=True)
    subject_id: int = Field(foreign_key="subject.id", index=True)

class Purchase(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.id", index=True)
    test_series_id: int = Field(foreign_key="testseries.id", index=True)
    purchased_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    expires_at: datetime

class QuizAttempt(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    user_id: int = Field(foreign_key="user.id", index=True)
    test_id: int = Field(foreign_key="test.id", index=True)
    started_at: datetime = Field(default_factory=datetime.now(timezone.utc))
    completed_at: datetime | None = Field(default=None)

class PromoCode(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    code: str = Field(index=True)
    test_series_id: int = Field(foreign_key="testseries.id", index=True)
    valid_from: datetime
    valid_until: datetime
    usage_limit: int
    usage_count: int = Field(default=0)
    user_limit: int

class PromoUsage(SQLModel, table=True):
    id: int | None = Field(primary_key=True, default=None)
    promo_code_id: int = Field(foreign_key="promocode.id", index=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    used_at: datetime = Field(default_factory=datetime.now(timezone.utc))
