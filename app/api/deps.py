from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.models.user import User
from app.schemas.token import TokenData
from app import crud  # Предположим, CRUD уже есть

# FastAPI будет искать токен в заголовке Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"/api/v1/auth/login")


async def get_current_user(
        db: AsyncSession = Depends(get_db),
        token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception

    user = await crud.user.get_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
