from app.database.session import SessionLocal
from app.modules.users.models import User
from app.modules.auth.security import hash_password

db = SessionLocal()

user = User(
    email="admin@escala.com",
    hashed_password=hash_password("123456")
)

db.add(user)
db.commit()
db.close()

print("Usuário criado")
