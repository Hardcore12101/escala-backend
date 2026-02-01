import sys
import os
from logging.config import fileConfig

from sqlalchemy import create_engine
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv

# =====================
# ENV
# =====================
load_dotenv(".env.docker")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL não definida")

# =====================
# PATH
# =====================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, BASE_DIR)

# =====================
# MODELS
# =====================
from src.app.database.base import Base

from src.app.modules.users.models import User
from src.app.models.company import Company
from src.app.modules.audit.models import AuditLog
from src.app.modules.obligations.models import Obligation
from src.app.modules.apurations.models import Apuration
from src.app.modules.tax_rules.models import TaxRule
from src.app.modules.tax_calculations.models import TaxCalculation
from src.app.modules.guides.models import Guide

# =====================
# ALEMBIC CONFIG
# =====================
config = context.config
config.set_main_option("sqlalchemy.url", DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

# =====================
# MIGRATIONS
# =====================
def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
