from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException

from app.database import Base, engine
from app.dependencies import verify_guild_master
from app.models import Bounty
from app.routers import bounties, guild


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan, title="Bounty Board API")

app.include_router(bounties.router)

app.include_router(guild.router,
                   prefix="/guild",
                   tags=["guild"],
                   dependencies=[Depends(verify_guild_master)])

@app.get("/health-check")
def health_check():
    return {"status": "Library API is online"}

