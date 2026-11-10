from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy import select

from app.dependencies import SearchDep, SessionDep, verify_guild_master
from app.models import Bounty
from app.schemas import BountyCreate, BountyPublic, BountySearchParams, BountyUpdate

router = APIRouter(
    prefix="/bounties",
    tags=["bounties"]
)

@router.post("/", response_model=BountyPublic, status_code=201,
        dependencies=[Depends(verify_guild_master)])
def create_bounty(bounty: BountyCreate,session: SessionDep):
    bounty_db = Bounty(**bounty.model_dump())
    session.add(bounty_db)

    session.commit()

    session.refresh(bounty_db)
    return bounty_db

@router.get("/", response_model=list[BountyPublic])
def get_all_bounties(session: SessionDep, filters: SearchDep):
    stmt = select(Bounty).where(Bounty.reward >= filters.min_reward)
    if filters.danger_level is not None:
        stmt = stmt.where(Bounty.danger_level == filters.danger_level)
    if filters.unclaimed_only:
        stmt = stmt.where(not Bounty.is_claimed)
    stmt = stmt.offset(filters.offset).limit(filters.limit)
    return  session.scalars(stmt).all()

@router.get("/{bounty_id}", response_model=BountyPublic)
def get_bounty(bounty_id: int, session: SessionDep):
    bounty = session.get(Bounty, bounty_id)
    if not bounty:
        raise HTTPException(status_code=404, detail="Bounty not found")
    return bounty

@router.patch("/{bounty_id}", response_model=BountyPublic,
            dependencies=[Depends(verify_guild_master)])
def update_bounty(session: SessionDep, bounty_id:int, bounty:BountyUpdate):
    bounty_db = session.get(Bounty, bounty_id)
    if not bounty_db:
        raise HTTPException(status_code=404, detail="Bounty not found")

    bounty_data = bounty.model_dump(exclude_unset=True)

    for k, v in bounty_data.items():
        setattr(bounty_db,k,v)
    session.commit()
    session.refresh(bounty_db)
    return bounty_db

@router.post("/{bounty_id}/claim", response_model=BountyPublic)
def claim_bounty(session: SessionDep, bounty_id: int,
                passcode: Annotated[str,Body(embed=True)]):
    bounty_db = session.get(Bounty, bounty_id)
    if not bounty_db:
        raise HTTPException(status_code=404, detail="Bounty not found")
    if bounty_db.is_claimed:
        raise HTTPException(status_code=400, detail="Bounty already claimed")

    if bounty_db.secret_passcode != passcode:
        raise HTTPException(status_code=403, detail="Invalid secret passcode")
    bounty_db.is_claimed = True

    session.commit()
    session.refresh(bounty_db)
    return bounty_db





