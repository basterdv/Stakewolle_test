import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app import crud
from app.schemas.user import UserCreate
from app.core.security import create_access_token, verify_password
from app.core.config import settings


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_new_user(self, user_in: UserCreate):
        # 1. Проверка существования пользователя
        existing_user = await crud.user.get_by_email(self.db, email=user_in.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )

        # 2. Опционально: Проверка email через Hunter.io
        if settings.HUNTER_API_KEY:
            is_valid = await self._verify_email_via_hunter(user_in.email)
            if not is_valid:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email address is invalid or disposable"
                )

        # 3. Логика реферального кода
        referrer_id = None
        if user_in.referral_code:
            ref_obj = await crud.referral.get_by_code(self.db, code=user_in.referral_code)
            if not ref_obj:
                raise HTTPException(status_code=404, detail="Referral code not found")

            # Проверка срока годности (в Middle+ это выносится в метод модели или сервис)
            from datetime import datetime, timezone
            if ref_obj.expires_at < datetime.now(timezone.utc):
                raise HTTPException(status_code=400, detail="Referral code expired")

            referrer_id = ref_obj.owner_id

        # 4. Создание пользователя
        new_user = await crud.user.create(self.db, obj_in=user_in, referrer_id=referrer_id)

        # 5. Опционально: Обогащение данных через Clearbit (Fire-and-forget или доп. логика)
        # В идеале это делается в фоне через Celery/TaskIQ, но для ТЗ сделаем асинхронный вызов
        if settings.CLEARBIT_API_KEY:
            # logic for enrichment...
            pass

        return new_user

    async def _verify_email_via_hunter(self, email: str) -> bool:
        """Интеграция с Hunter.io"""
        async with httpx.AsyncClient() as client:
            try:
                url = f"https://api.emailhunter.co{email}&api_key={settings.HUNTER_API_KEY}"
                response = await client.get(url, timeout=5.0)
                if response.status_code == 200:
                    data = response.json()
                    return data["data"]["status"] != "invalid"
                return True  # Если сервис недоступен, пропускаем
            except Exception:
                return True

    async def authenticate(self, email: str, password: str):
        user = await crud.user.get_by_email(self.db, email=email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user
