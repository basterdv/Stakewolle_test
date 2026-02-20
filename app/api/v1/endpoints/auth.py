from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app import schemas
from app.db.session import get_db
from app.services.auth_service import AuthService
from app.core import security

router = APIRouter()


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
async def register(
        user_in: schemas.UserCreate,
        db: AsyncSession = Depends(get_db)
):
    auth_service = AuthService(db)
    return await auth_service.register_new_user(user_in)


@router.post("/login", response_model=schemas.Token)
async def login(
        db: AsyncSession = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()
):
    auth_service = AuthService(db)
    user = await auth_service.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = security.create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}
