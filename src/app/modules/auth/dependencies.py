from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from src.app.core.security import oauth2_scheme
from src.app.core.config import settings
from src.app.database.dependencies import get_db
from src.app.modules.users.models import User
from src.app.modules.audit.service import log_event
from uuid import UUID



def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido ou expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        user_id: str | None = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == UUID(user_id)).first()
    if user is None:
        raise credentials_exception

    try:
        log_event(
            db,
            action="ACCESS_ROUTE",
            entity="user",
            entity_id=user.id,
            user_id=user.id,
        )
    except Exception as e:
        db.rollback()
        # opcional: logger.warning(e)

    return user
