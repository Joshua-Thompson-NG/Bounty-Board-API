from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Bounty(Base):
    __tablename__ = "bounties"

    id: Mapped[int] = mapped_column(primary_key=True)
    target_name: Mapped[str] = mapped_column(index=True)
    danger_level: Mapped[str] = mapped_column(index=True)
    reward: Mapped[int]
    is_claimed: Mapped[bool] = mapped_column(default=False)
    secret_passcode: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

