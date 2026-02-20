from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    # ID того, кто пригласил данного пользователя
    referrer_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))

    # Связь "один-к-одному" с реферальным кодом (у юзера может быть только 1 активный код)
    referral_code: Mapped["ReferralCode"] = relationship(
        back_populates="owner",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # Список тех, кого пригласил этот пользователь
    referrals: Mapped[list["User"]] = relationship()
