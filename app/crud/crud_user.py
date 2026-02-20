from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
from app.crud.base import CRUDBase

class CRUDUser(CRUDBase[User]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> User | None:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, *, obj_in: UserCreate, referrer_id: int | None = None) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            referrer_id=referrer_id
        )
        db.add(db_obj)
        await db.flush() # Получаем ID без коммита всей транзакции
        return db_obj

user = CRUDUser(User)
