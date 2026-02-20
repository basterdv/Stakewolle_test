import redis.asyncio as redis
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas, models
from app.db.session import get_db
from app.db.redis import get_redis # Наш генератор клиента Redis
from app.services.referral_service import ReferralService
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/code", response_model=schemas.ReferralCodeOut)
async def create_my_code(
    code_in: schemas.ReferralCodeCreate,
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    cache: redis.Redis = Depends(get_redis)
):
    service = ReferralService(db, cache)
    return await service.create_code(current_user, code_in)

@router.delete("/code", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_code(
    current_user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    cache: redis.Redis = Depends(get_redis)
):
    service = ReferralService(db, cache)
    await service.delete_code(current_user)

@router.get("/code-by-email", response_model=str)
async def get_code_by_email(
    email: str,
    db: AsyncSession = Depends(get_db),
    cache: redis.Redis = Depends(get_redis)
):
    service = ReferralService(db, cache)
    return await service.get_code_by_email(email)
