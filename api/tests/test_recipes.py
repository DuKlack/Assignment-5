from ..controllers import recipe
import pytest
from ..models import models, schemas

@pytest.fixture
def db_session(mocker):
    return mocker.Mock()

def test_create_recipe(db_session):
    recipe_data = {"sandwich_id": 1, "resource_id": 1, "amount": 2}
    recipe_object = models.Recipe(**recipe_data)
    db_session.refresh.side_effect = lambda obj: setattr(obj, 'id', 1)

    created = recipe.create(db_session, recipe_object)
    assert created is not None
    assert created.sandwich_id == 1
    assert created.resource_id == 1
    assert created.amount == 2

def test_read_all_recipes(db_session):
    mock_recipes = [
        models.Recipe(id=1, sandwich_id=1, resource_id=1, amount=2),
    ]
    db_session.query.return_value.all.return_value = mock_recipes

    result = recipe.read_all(db_session)
    assert len(result) == 1
    assert result[0].amount == 2

def test_read_one_recipe(db_session):
    mock_recipe = models.Recipe(id=1, sandwich_id=1, resource_id=1, amount=2)
    db_session.query.return_value.filter.return_value.first.return_value = mock_recipe

    result = recipe.read_one(db_session, 1)
    assert result is not None
    assert result.id == 1

def test_update_recipe(db_session):
    recipe_update = schemas.RecipeUpdate(amount=3)
    mock_recipe = models.Recipe(id=1, sandwich_id=1, resource_id=1, amount=2)
    db_query_mock = db_session.query.return_value.filter.return_value
    db_query_mock.first.return_value = mock_recipe

    updated = recipe.update(db_session, 1, recipe_update)
    db_query_mock.update.assert_called_once()
    db_session.commit.assert_called_once()

def test_delete_recipe(db_session):
    db_query_mock = db_session.query.return_value.filter.return_value
    response = recipe.delete(db_session, 1)
    db_query_mock.delete.assert_called_once()
    db_session.commit.assert_called_once()
    assert response.status_code == 204