from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime, timezone

class ReferralCodeBase(BaseModel):
    code: str
    expires_at: datetime

class ReferralCodeCreate(BaseModel):
    code: str
    expires_at: datetime

    @field_validator("expires_at")
    @classmethod
    def prevent_past_expiration(cls, v: datetime) -> datetime:
        if v <= datetime.now(timezone.utc):
            raise ValueError("Expiration date must be in the future")
        return v

class ReferralCodeOut(ReferralCodeBase):
    owner_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
