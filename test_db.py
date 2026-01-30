from app.database.session import engine

print("Conectando ao banco...")
engine.connect()
print("Conexão OK")
