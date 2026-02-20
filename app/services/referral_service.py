import json
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime, timezone

from app import crud
from app.models.user import User
from app.schemas.referral import ReferralCodeCreate
from app.core.config import settings


class ReferralService:
    def __init__(self, db: AsyncSession, redis_client: redis.Redis):
        self.db = db
        self.redis = redis_client
        self.cache_prefix = "ref_code:"

    async def create_code(self, user: User, code_in: ReferralCodeCreate):
        # 1. Проверяем, нет ли уже активного кода (Middle: логика на уровне БД + проверка тут)
        existing = await crud.referral.get_by_owner_id(self.db, owner_id=user.id)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already has an active referral code. Delete it first."
            )

        # 2. Проверяем уникальность самого кода строки
        code_exists = await crud.referral.get_by_code(self.db, code=code_in.code)
        if code_exists:
            raise HTTPException(status_code=400, detail="This code string is already taken")

        # 3. Сохраняем в БД
        new_code = await crud.referral.create_with_owner(self.db, obj_in=code_in, owner_id=user.id)

        # 4. Кэшируем в Redis (Middle: рассчитываем TTL кэша на основе expires_at)
        ttl = int((code_in.expires_at - datetime.now(timezone.utc)).total_seconds())
        if ttl > 0:
            await self.redis.set(
                f"{self.cache_prefix}{user.email}",
                new_code.code,
                ex=ttl
            )

        return new_code

    async def get_code_by_email(self, email: str) -> str:
        # 1. Сначала идем в Redis (Cache Aside pattern)
        cached_code = await self.redis.get(f"{self.cache_prefix}{email}")
        if cached_code:
            return cached_code.decode("utf-8")

        # 2. Если в кэше нет, идем в БД
        user = await crud.user.get_by_email(self.db, email=email)
        if not user or not user.referral_code:
            raise HTTPException(status_code=404, detail="Referral code not found for this email")

        # Проверка срока годности в БД
        if user.referral_code.expires_at < datetime.now(timezone.utc):
            raise HTTPException(status_code=404, detail="Referral code expired")

        # 3. Обновляем кэш перед возвратом
        ttl = int((user.referral_code.expires_at - datetime.now(timezone.utc)).total_seconds())
        await self.redis.set(f"{self.cache_prefix}{email}", user.referral_code.code, ex=ttl)

        return user.referral_code.code

    async def delete_code(self, user: User):
        code_obj = await crud.referral.get_by_owner_id(self.db, owner_id=user.id)
        if not code_obj:
            raise HTTPException(status_code=404, detail="No active code to delete")

        # Удаляем из БД
        await crud.referral.remove(self.db, id=code_obj.id)
        # Удаляем из Redis
        await self.redis.delete(f"{self.cache_prefix}{user.email}")
