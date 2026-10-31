from ..controllers import order_detail
import pytest
from ..models import models, schemas

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_order_detail(db_session):
    detail_data = {"order_id": 1, "sandwich_id": 1, "amount": 2}
    detail_object = models.OrderDetail(**detail_data)
    db_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 1)

    created = order_detail.create(db_session, detail_object)
    assert created is not None
    assert created.order_id == 1
    assert created.sandwich_id == 1
    assert created.amount == 2

def test_read_all_order_details(db_session):
    mock_details = [
        models.OrderDetail(id=1, order_id=1, sandwich_id=1, amount=2),
    ]
    db_session.query.return_value.all.return_value = mock_details

    result = order_detail.read_all(db_session)
    assert len(result) == 1
    assert result[0].amount == 2

def test_read_one_order_detail(db_session):
    mock_detail = models.OrderDetail(id=1, order_id=1, sandwich_id=1, amount=2)
    db_session.query.return_value.filter.return_value.first.return_value = mock_detail

    result = order_detail.read_one(db_session, 1)
    assert result is not None
    assert result.id == 1

def test_update_order_detail(db_session):
    detail_update = schemas.OrderDetailUpdate(amount=5)
    mock_detail = models.OrderDetail(id=1, order_id=1, sandwich_id=1, amount=2)
    db_query_mock = db_session.query.return_value.filter.return_value
    db_query_mock.first.return_value = mock_detail

    updated = order_detail.update(db_session, 1, detail_update)
    db_query_mock.update.assert_called_once()
    db_session.commit.assert_called_once()

def test_delete_order_detail(db_session):
    db_query_mock = db_session.query.return_value.filter.return_value
    response = order_detail.delete(db_session, 1)
    db_query_mock.delete.assert_called_once()
    db_session.commit.assert_called_once()
    assert response.status_code == 204