from fastapi import APIRouter

# Domínio
from src.app.modules.auth.router import router as auth_router
from src.app.modules.users.router import router as users_router
from src.app.modules.companies.router import router as companies_router
from src.app.modules.obligations.router import router as obligations_router
from src.app.modules.tax_rules.router import router as tax_rules_router
from src.app.modules.tax_calculations.router import router as tax_calculations_router
from src.app.modules.apurations.router import router as apurations_router
from src.app.modules.guides.router import router as guides_router
from src.app.modules.guides.pdf_router import router as guides_pdf_router
from src.app.modules.dashboard.router import router as dashboard_router

# Rotas técnicas
from src.app.routes.me import router as me_router


api_router = APIRouter(prefix="/api")

# Auth / Usuários
api_router.include_router(auth_router)
api_router.include_router(users_router)

# Empresas
api_router.include_router(companies_router)

# Fiscal / Tributário
api_router.include_router(obligations_router)
api_router.include_router(tax_rules_router)
api_router.include_router(tax_calculations_router)
api_router.include_router(apurations_router)

# Guias / PDFs
api_router.include_router(guides_router)
api_router.include_router(guides_pdf_router)

# Dashboard
api_router.include_router(dashboard_router)

# Técnico autenticado
api_router.include_router(me_router)

@api_router.get("/")
def root():
    return {"message": "Escala API online"}
