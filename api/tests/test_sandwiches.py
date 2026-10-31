from ..controllers import sandwich
import pytest
from ..models import models, schemas

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_sandwich(db_session):
    sandwich_data = {"sandwich_name": "BLT", "price": 5.99}
    sandwich_object = models.Sandwich(**sandwich_data)
    db_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 1)

    created = sandwich.create(db_session, sandwich_object)
    assert created is not None
    assert created.sandwich_name == "BLT"
    assert created.price == 5.99

def test_read_all_sandwiches(db_session):
    mock_sandwiches = [
        models.Sandwich(id=1, sandwich_name="BLT", price=5.99),
        models.Sandwich(id=2, sandwich_name="Ham & Cheese", price=6.49)
    ]
    db_session.query.return_value.all.return_value = mock_sandwiches

    result = sandwich.read_all(db_session)
    assert len(result) == 2
    assert result[0].sandwich_name == "BLT"

def test_read_one_sandwich(db_session):
    mock_sandwich = models.Sandwich(id=1, sandwich_name="BLT", price=5.99)
    db_session.query.return_value.filter.return_value.first.return_value = mock_sandwich

    result = sandwich.read_one(db_session, 1)
    assert result is not None
    assert result.id == 1
    assert result.sandwich_name == "BLT"

def test_update_sandwich(db_session):
    sandwich_update = schemas.SandwichUpdate(price=6.99)
    mock_sandwich = models.Sandwich(id=1, sandwich_name="BLT", price=5.99)
    db_query_mock = db_session.query.return_value.filter.return_value
    db_query_mock.first.return_value = mock_sandwich

    updated = sandwich.update(db_session, 1, sandwich_update)
    db_query_mock.update.assert_called_once()
    db_session.commit.assert_called_once()

def test_delete_sandwich(db_session):
    db_query_mock = db_session.query.return_value.filter.return_value
    response = sandwich.delete(db_session, 1)
    db_query_mock.delete.assert_called_once()
    db_session.commit.assert_called_once()
    assert response.status_code == 204