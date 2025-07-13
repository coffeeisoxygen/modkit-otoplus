import sys
import os
from logging.config import fileConfig

from alembic import context

# Setup path biar bisa import dari src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# Import engine & model
from src.backend.db import engine
from src.backend.models.member import Member # noqa: F401
from sqlmodel import SQLModel

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata buat autogenerate
target_metadata = SQLModel.metadata


def run_migrations_offline():
    context.configure(
        url=engine.url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
