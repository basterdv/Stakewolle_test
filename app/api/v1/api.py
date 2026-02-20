from fastapi import APIRouter
from app.api.v1.endpoints import auth, referrals, users

api_router = APIRouter()

# Регистрация и логин
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# Управление реферальными кодами (создание, удаление, поиск)
api_router.include_router(
    referrals.router,
    prefix="/referrals",
    tags=["Referral Codes"]
)

# Информация о рефери (получение списка приглашенных по ID)
# Эндпоинт: GET /api/v1/users/{id}/referrals
api_router.include_router(
    users.router,
    prefix="/users",
    tags=["Users & Referrals"]
)
