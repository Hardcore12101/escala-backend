import src.app.models
from sqlalchemy.orm import Session
from src.app.database.session import SessionLocal
from src.app.modules.users.models import User
from src.app.core.security import get_password_hash

ADMIN_EMAIL = "admin@escaladigital.com"
ADMIN_PASSWORD = "admin123"  # depois trocamos via env

def run():
    db: Session = SessionLocal()

    user = db.query(User).filter(User.email == ADMIN_EMAIL).first()
    if user:
        print("Admin já existe")
        return

    admin = User(
        email=ADMIN_EMAIL,
        hashed_password=get_password_hash(ADMIN_PASSWORD),
        is_active=True,
        is_superuser=True,
    )

    db.add(admin)
    db.commit()
    db.refresh(admin)

    print("Admin criado com sucesso")

if __name__ == "__main__":
    run()
