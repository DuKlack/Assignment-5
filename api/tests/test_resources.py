from ..controllers import Resource as resource_controller
import pytest
from ..models import models, schemas

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_resource(db_session):
    res_data = {"item": "Tomato", "amount": 100}
    res_object = models.Resource(**res_data)
    db_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 1)

    created = resource_controller.create(db_session, res_object)
    assert created is not None
    assert created.item == "Tomato"
    assert created.amount == 100

def test_read_all_resources(db_session):
    mock_resources = [
        models.Resource(id=1, item="Tomato", amount=100),
        models.Resource(id=2, item="Lettuce", amount=50)
    ]
    db_session.query.return_value.all.return_value = mock_resources

    result = resource_controller.read_all(db_session)
    assert len(result) == 2
    assert result[0].item == "Tomato"

def test_read_one_resource(db_session):
    mock_res = models.Resource(id=1, item="Tomato", amount=100)
    db_session.query.return_value.filter.return_value.first.return_value = mock_res

    result = resource_controller.read_one(db_session, 1)
    assert result is not None
    assert result.id == 1
    assert result.item == "Tomato"

def test_update_resource(db_session):
    res_update = schemas.ResourceUpdate(amount=120)
    mock_res = models.Resource(id=1, item="Tomato", amount=100)
    db_query_mock = db_session.query.return_value.filter.return_value
    db_query_mock.first.return_value = mock_res

    updated = resource_controller.update(db_session, 1, res_update)
    db_query_mock.update.assert_called_once()
    db_session.commit.assert_called_once()

def test_delete_resource(db_session):
    db_query_mock = db_session.query.return_value.filter.return_value
    response = resource_controller.delete(db_session, 1)
    db_query_mock.delete.assert_called_once()
    db_session.commit.assert_called_once()
    assert response.status_code == 204