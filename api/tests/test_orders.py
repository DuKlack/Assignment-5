from fastapi.testclient import TestClient
from ..controllers import orders
from ..main import app
import pytest
from ..models import models, schemas

client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_order(db_session):
    order_data = {
        "customer_name": "John Doe",
        "description": "Test order"
    }
    order_object = models.Order(**order_data)

    db_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 1)

    created_order = orders.create(db_session, order_object)

    assert created_order is not None
    assert created_order.customer_name == "John Doe"
    assert created_order.description == "Test order"

def test_read_all_orders(db_session):
    mock_orders = [
        models.Order(id=1, customer_name="Alice", description="Order 1"),
        models.Order(id=2, customer_name="Bob", description="Order 2")
    ]
    db_session.query.return_value.all.return_value = mock_orders

    result = orders.read_all(db_session)

    assert len(result) == 2
    assert result[0].customer_name == "Alice"
    assert result[1].customer_name == "Bob"

def test_read_one_order(db_session):
    mock_order = models.Order(id=1, customer_name="Alice", description="Order 1")
    db_session.query.return_value.filter.return_value.first.return_value = mock_order

    result = orders.read_one(db_session, 1)

    assert result is not None
    assert result.id == 1
    assert result.customer_name == "Alice"

def test_update_order(db_session):
    order_update = schemas.OrderUpdate(customer_name="Alice Updated", description="Updated description")
    mock_order = models.Order(id=1, customer_name="Alice", description="Order 1")
    
    db_query_mock = db_session.query.return_value.filter.return_value
    db_query_mock.first.return_value = mock_order

    updated_order = orders.update(db_session, 1, order_update)

    db_query_mock.update.assert_called_once()
    db_session.commit.assert_called_once()

def test_delete_order(db_session):
    db_query_mock = db_session.query.return_value.filter.return_value

    response = orders.delete(db_session, 1)

    db_query_mock.delete.assert_called_once()
    db_session.commit.assert_called_once()
    assert response.status_code == 204