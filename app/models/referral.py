import datetime
from sqlalchemy import String, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from app.models.base import Base


class ReferralCode(Base):
    __tablename__ = "referral_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    expires_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    # Владелец кода
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,  # Гарантирует "1 пользователь = 1 код" на уровне БД
        nullable=False
    )

    owner: Mapped["User"] = relationship(back_populates="referral_code")

    # Индекс для ускорения проверки срока годности при фильтрации
    __table_args__ = (
        Index("ix_referral_codes_code_expires", "code", "expires_at"),
    )
