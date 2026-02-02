from alembic import context
from sqlalchemy import engine_from_config, pool
from backend.database import Base, engine  # import your SQLAlchemy Base + engine

# Alembic Config object, provides access to values in alembic.ini
config = context.config

# Target metadata for autogenerate (your models)
target_metadata = Base.metadata

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    context.configure(
        url=str(engine.url),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

# Alembic will call one of these depending on mode
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()