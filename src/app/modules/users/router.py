from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from src.app.database.dependencies import get_db
from src.app.modules.auth.dependencies import get_current_user
from src.app.modules.users.models import User
from src.app.modules.users.schemas import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from src.app.modules.users.service import (
    create_user,
    update_user,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserResponse)
def read_me(
    current_user: User = Depends(get_current_user),
):
    """
    Retorna o usuário autenticado
    """
    return current_user


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_user(
    data: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Criação de usuário (signup)
    Não requer autenticação
    """
    return create_user(db, data)


@router.get(
    "",
    response_model=list[UserResponse],
)
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Lista usuários do sistema
    (temporário – depois pode ser restringido)
    """
    return db.query(User).all()


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
)
def update_user_route(
    user_id: UUID,
    data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Atualiza um usuário.
    Regra atual:
    - usuário só pode atualizar a si mesmo
    """
    if current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não pode alterar outro usuário",
        )

    try:
        return update_user(db, user_id, data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
