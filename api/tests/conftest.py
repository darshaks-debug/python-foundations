import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from expense_api import app, Base, get_db

# Use an in-memory SQLite database for testing (fast and isolated)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create the tables before running tests
Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Yields a fresh database session for each test."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Clean up tables after each test so they don't leak into the next
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Overrides the get_db dependency to use the test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()