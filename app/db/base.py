# Импортируем декларативную базу
from app.models.base import Base

# Импортируем все модели, чтобы они зарегистрировались в Base.metadata
from app.models.user import User
from app.models.referral import ReferralCode

# Теперь Base.metadata содержит информацию обо всех таблицах
