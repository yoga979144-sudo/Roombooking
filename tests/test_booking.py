import pytest
from app import app, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_successful_booking(client):
    payload = {"room_id": "A1", "start_time": "2024-10-10T10:00:00", "end_time": "2024-10-10T11:00:00"}
    rv = client.post('/book', json=payload)
    assert rv.status_code == 201

def test_double_booking_fails(client):
    payload = {"room_id": "A1", "start_time": "2024-10-10T10:00:00", "end_time": "2024-10-10T11:00:00"}
    client.post('/book', json=payload)
    # Try booking an overlapping slot
    rv = client.post('/book', json=payload)
    assert rv.status_code == 409
@pytest.fixture
def client():
    app.config['TESTING'] = True
    # This ensures we use a fresh in-memory database for every test run
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.drop_all()  # Add this to clear existing data
            db.create_all()
        yield client
