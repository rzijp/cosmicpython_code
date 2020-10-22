import pytest
from allocation.adapters.orm import start_mappers, metadata
from allocation.config import get_postgres_uri
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker
from sqlalchemy.orm.session import sessionmaker


@pytest.fixture
def postgres_db():
    engine = create_engine(get_postgres_uri())
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(postgres_db):
    start_mappers()
    session = sessionmaker(bind=postgres_db)()
    session.execute("TRUNCATE TABLE batches CASCADE")
    session.commit()
    yield session
    clear_mappers()
