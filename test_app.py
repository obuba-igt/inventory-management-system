from unittest.mock import patch, MagicMock
from app import app, inventory
import external_api
import pytest


@pytest.fixture
def client():
    app.config['TESTING'] = True
    inventory.clear()
    import app as app_module
    app_module.id_counter = 1
    with app.test_client() as c:
        yield c


def test_get_empty(client):
    resp = client.get('/inventory')
    assert resp.status_code == 200
    assert resp.get_json() == []


def test_post_and_get(client):
    with patch('app.fetch_from_openfoodfacts', return_value={}):
        resp = client.post(
            '/inventory', json={"product_name": "Milk", "quantity": 5, "price": 2.5})
        assert resp.status_code == 201
        assert resp.get_json()["id"] == 1
        resp2 = client.get('/inventory/1')
        assert resp2.status_code == 200


def test_patch(client):
    with patch('app.fetch_from_openfoodfacts', return_value={}):
        client.post('/inventory', json={"product_name": "Bread"})
        resp = client.patch('/inventory/1', json={"quantity": 10})
        assert resp.status_code == 200
        assert resp.get_json()["quantity"] == 10


def test_delete(client):
    with patch('app.fetch_from_openfoodfacts', return_value={}):
        client.post('/inventory', json={"product_name": "Bread"})
        resp = client.delete('/inventory/1')
        assert resp.status_code == 200
        resp2 = client.get('/inventory/1')
        assert resp2.status_code == 404


def test_external_barcode_mock():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"status": 1, "product": {
        "product_name": "Organic Almond Milk", "brands": "silk", "ingredients_text": "water, almonds"}}
    mock_resp.raise_for_status.return_value = None
    with patch('external_api.requests.get', return_value=mock_resp):
        result = external_api.fetch_from_openfoodfacts(barcode="123")
        assert result["product_name"] == "Organic Almond Milk"
        assert result["brands"] == "silk"


def test_external_search_mock():
    mock_resp = MagicMock()
    mock_resp.json.return_value = {"products": [
        {"product_name": "Coca Cola", "brands": "Coca-Cola", "ingredients_text": "water sugar"}]}
    mock_resp.raise_for_status.return_value = None
    with patch('external_api.requests.get', return_value=mock_resp):
        result = external_api.fetch_from_openfoodfacts(
            product_name="Coca Cola")
        assert "Coca" in result["product_name"]
