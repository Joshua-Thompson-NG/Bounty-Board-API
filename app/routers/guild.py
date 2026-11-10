from fastapi import APIRouter, HTTPException

from app.dependencies import SessionDep
from app.models import Bounty

router = APIRouter()

@router.delete("/bounties/{bounty_id}")
def delete_bounty(bounty_id: int, session: SessionDep):
    bounty_db = session.get(Bounty, bounty_id)
    if not bounty_db:
        raise HTTPException(status_code=404, detail="Bounty not found")

    session.delete(bounty_db)
    session.commit()
    return {"message": "Bounty deleted"}