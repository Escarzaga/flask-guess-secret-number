import os
import pytest
from main import app, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    os.environ["DATABASE_URL"] = "sqlite:///:memory:" #lo almacena en memoria y una vez que temrine lo borra
    client = app.test_client()

    cleanup()  # clean up before every test

    db.create_all()

    yield client  #


def test_index_not_logged_in(client): #siempre deben empezar con test_
    response = client.get('/')
    assert b'Enter your name' in response.data


def test_index_logged_in(client):
    client.post('/login', data={"user-name": "Test User", "user-email": "test@user.com",
                                "user-password": "password123"}, follow_redirects=True)

    response = client.get('/')
    assert b'Enter your guess' in response.data


def cleanup():
    # clean up/delete the DB (drop all tables in the database)
    db.drop_all()


#pytest tests/test_main.py -p no:warnings   esta línea es para ejecutar en la terminal el test, por que la instruccion
# de ramuta no funciona, asi ya pasa el test y no da error

