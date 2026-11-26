import os

from alembic import context
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.pool import NullPool

dsn = os.environ.get("G20_DATABASE_URL")
if not dsn:
    raise RuntimeError("Set G20_DATABASE_URL to the G20 corpus database.")

url = make_url(dsn)
if url.get_backend_name() not in {"postgres", "postgresql"}:
    raise RuntimeError("G20_DATABASE_URL must point to PostgreSQL.")
url = url.set(drivername="postgresql+psycopg")

if context.is_offline_mode():
    context.configure(url=url, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()
else:
    engine = create_engine(url, poolclass=NullPool)
    with engine.connect() as connection:
        context.configure(connection=connection)
        with context.begin_transaction():
            context.run_migrations()
