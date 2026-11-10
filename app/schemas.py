from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

DangerLevel = Literal["low","high","extreme"]

class BountyBase(BaseModel):
    target_name: str
    danger_level: DangerLevel = "low"
    reward: int = Field(gt=0)

class BountyCreate(BountyBase):
    secret_passcode: str

class BountyUpdate(BaseModel):
    target_name: str | None = None
    danger_level: DangerLevel | None = None
    reward: int | None = Field(default=None, gt=0)
    is_claimed: bool | None = None

class BountyPublic(BountyBase):
    id: int
    is_claimed: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class BountySearchParams:
    def __init__(self, danger_level: DangerLevel | None = None, unclaimed_only:
    bool = False, min_reward: int = 0, offset: int = 0, limit: int = 10):
        self.danger_level = danger_level
        self.unclaimed_only = unclaimed_only
        self.min_reward = min_reward
        self.offset = offset
        self.limit = limit