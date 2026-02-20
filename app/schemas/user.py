from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str
    referral_code: Optional[str] = None  # Код, по которому регистрируемся


class UserOut(UserBase):
    id: int
    referrer_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)  # Заменяет orm_mode=True в v2


class UserReferralInfo(UserOut):
    # Для эндпоинта получения списка рефералов
    pass
