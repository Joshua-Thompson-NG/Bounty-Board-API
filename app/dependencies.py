from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.schemas import BountySearchParams


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_guild_master(x_guild_key: Annotated[str | None, Header()] = None,):
    if x_guild_key != "master-secret-key":
        raise HTTPException(status_code=403, detail="X-Guild-Key header required")

SessionDep = Annotated[Session, Depends(get_db)]
SearchDep = Annotated[BountySearchParams, Depends()]

