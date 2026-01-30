from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from src.app.routes.health import router as health_router
from src.app.api import api_router
from src.app.database.session import SessionLocal
from src.app.database.seed import seed_system_company
from sqlalchemy.exc import OperationalError

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(api_router)
