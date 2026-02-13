from sqlalchemy import create_engine, StaticPool
from fastapi.testclient import TestClient
import pytest
import uuid
from . import schema
from .main import app
from .schema import get_connection


# DB_PATH = "tests_database.db"
# if os.path.exists(DB_PATH):
#     os.remove(DB_PATH)

@pytest.fixture()
def engine():
    test_engine = create_engine(
                            f"sqlite:///:memory:",
                            connect_args={"check_same_thread":False},
                            poolclass=StaticPool) 

    schema.meta.create_all(test_engine)
    with test_engine.begin() as conn:
        conn.execute(schema.categories.insert().values(name="Electronics"))
        conn.execute(schema.categories.insert().values(name="Food"))
    
    yield test_engine

@pytest.fixture()
def client(engine):
    def get_conn_overide():
        with engine.begin() as conn:
            yield conn
    app.dependency_overrides[get_connection] = get_conn_overide
    with TestClient(app) as client:
        yield client


@pytest.fixture()
def auth_token(client):
    email = f'user_{uuid.uuid4()}@gamil.com'
    response = client.post(
        "/auth/register",
        json={"email":email, "password":'12345678', "name":'Mohamed'}
    )
    assert response.status_code == 200
    return {"token":response.json()['access_token'], "email":email, "password":'12345678'}

@pytest.fixture()
def seller_token(auth_token, client):
    response = client.post(
        "/seller/new",
        headers={"auth":auth_token['token']},
        json={"name":"Mohamed's Shop"}
    )
    assert response.status_code == 200
    seller_Token = response.json()['access_token']
    assert seller_Token
    return {"token":response.json()['access_token'], "email":auth_token["email"], "password":'12345678'}
