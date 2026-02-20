from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.referral import ReferralCode
from app.schemas.referral import ReferralCodeCreate
from app.crud.base import CRUDBase

class CRUDReferral(CRUDBase[ReferralCode]):
    async def get_by_code(self, db: AsyncSession, *, code: str) -> ReferralCode | None:
        result = await db.execute(select(ReferralCode).where(ReferralCode.code == code))
        return result.scalar_one_or_none()

    async def get_by_owner_id(self, db: AsyncSession, *, owner_id: int) -> ReferralCode | None:
        result = await db.execute(select(ReferralCode).where(ReferralCode.owner_id == owner_id))
        return result.scalar_one_or_none()

    async def create_with_owner(
        self, db: AsyncSession, *, obj_in: ReferralCodeCreate, owner_id: int
    ) -> ReferralCode:
        db_obj = ReferralCode(
            **obj_in.model_dump(),
            owner_id=owner_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

referral = CRUDReferral(ReferralCode)
