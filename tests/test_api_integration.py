"""
API Integration Tests - 20 Sample Tests with Random Failures
"""
import pytest
from tests.fake_api_client import APIException


@pytest.mark.api
@pytest.mark.smoke
def test_get_user_list(api_client):
    """Test GET /users - Retrieve list of users"""
    response = api_client.get("/users")
    assert response.status_code == 200
    assert response.ok
    assert "status" in response.json()


@pytest.mark.api
def test_get_user_by_id(api_client, test_user_data):
    """Test GET /users/{id} - Retrieve specific user"""
    user_id = test_user_data["id"]
    response = api_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.ok


@pytest.mark.api
def test_create_user(api_client, test_user_data):
    """Test POST /users - Create a new user"""
    response = api_client.post("/users", data=test_user_data)
    assert response.status_code == 201
    assert "id" in response.json()


@pytest.mark.api
def test_update_user(api_client, test_user_data):
    """Test PUT /users/{id} - Update existing user"""
    user_id = test_user_data["id"]
    response = api_client.put(f"/users/{user_id}", data=test_user_data)
    assert response.status_code == 200
    assert response.ok


@pytest.mark.api
def test_delete_user(api_client):
    """Test DELETE /users/{id} - Delete a user"""
    user_id = 123
    response = api_client.delete(f"/users/{user_id}")
    assert response.status_code == 204


@pytest.mark.api
@pytest.mark.smoke
def test_get_product_list(api_client):
    """Test GET /products - Retrieve list of products"""
    response = api_client.get("/products")
    assert response.status_code == 200
    assert response.ok


@pytest.mark.api
def test_get_product_by_id(api_client, test_product_data):
    """Test GET /products/{id} - Retrieve specific product"""
    product_id = test_product_data["id"]
    response = api_client.get(f"/products/{product_id}")
    assert response.status_code == 200


@pytest.mark.api
def test_create_product(api_client, test_product_data):
    """Test POST /products - Create a new product"""
    response = api_client.post("/products", data=test_product_data)
    assert response.status_code == 201
    assert "id" in response.json()


@pytest.mark.api
def test_update_product(api_client, test_product_data):
    """Test PUT /products/{id} - Update existing product"""
    product_id = test_product_data["id"]
    response = api_client.put(f"/products/{product_id}", data=test_product_data)
    assert response.status_code == 200


@pytest.mark.api
def test_patch_product_price(api_client):
    """Test PATCH /products/{id} - Partially update product price"""
    product_id = 456
    response = api_client.patch(f"/products/{product_id}", data={"price": 99.99})
    assert response.status_code == 200


@pytest.mark.api
@pytest.mark.smoke
def test_get_order_list(api_client):
    """Test GET /orders - Retrieve list of orders"""
    response = api_client.get("/orders")
    assert response.status_code == 200
    assert response.ok


@pytest.mark.api
def test_get_order_by_id(api_client, test_order_data):
    """Test GET /orders/{id} - Retrieve specific order"""
    order_id = test_order_data["id"]
    response = api_client.get(f"/orders/{order_id}")
    assert response.status_code == 200


@pytest.mark.api
def test_create_order(api_client, test_order_data):
    """Test POST /orders - Create a new order"""
    response = api_client.post("/orders", data=test_order_data)
    assert response.status_code == 201
    assert "id" in response.json()


@pytest.mark.api
def test_update_order_status(api_client):
    """Test PATCH /orders/{id}/status - Update order status"""
    order_id = 789
    response = api_client.patch(f"/orders/{order_id}/status", data={"status": "shipped"})
    assert response.status_code == 200


@pytest.mark.api
def test_cancel_order(api_client):
    """Test DELETE /orders/{id} - Cancel an order"""
    order_id = 101
    response = api_client.delete(f"/orders/{order_id}")
    assert response.status_code == 204


@pytest.mark.api
@pytest.mark.regression
def test_search_products(api_client):
    """Test GET /products/search - Search products by query"""
    response = api_client.get("/products/search", params={"q": "laptop"})
    assert response.status_code == 200
    assert response.ok


@pytest.mark.api
@pytest.mark.regression
def test_get_user_orders(api_client):
    """Test GET /users/{id}/orders - Get orders for specific user"""
    user_id = 555
    response = api_client.get(f"/users/{user_id}/orders")
    assert response.status_code == 200


@pytest.mark.api
def test_add_product_to_cart(api_client):
    """Test POST /cart/items - Add product to shopping cart"""
    cart_data = {"product_id": 123, "quantity": 2}
    response = api_client.post("/cart/items", data=cart_data)
    assert response.status_code == 201


@pytest.mark.api
def test_get_cart_contents(api_client):
    """Test GET /cart - Retrieve shopping cart contents"""
    response = api_client.get("/cart")
    assert response.status_code == 200
    assert response.ok


@pytest.mark.api
def test_checkout_cart(api_client, test_order_data):
    """Test POST /checkout - Complete checkout process"""
    response = api_client.post("/checkout", data=test_order_data)
    assert response.status_code == 201
    assert "id" in response.json()
