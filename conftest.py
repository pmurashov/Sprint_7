import pytest
from api.api_client import APIClient

@pytest.fixture(scope="class")
def api_client():
    return APIClient()


@pytest.fixture(scope="class")
def required_fields():
    return ["id", "firstName", "lastName", "address", "metroStation", "phone",
            "rentTime", "deliveryDate", "track", "color", "comment", "createdAt",
            "updatedAt", "status"]

@pytest.fixture(scope='function')
def clear_courier_data():
    def _clear_courier_data(api_client, login, password):
        courier_id = api_client.courier_login(login, password).json().get("id")
        api_client.delete_courier(courier_id)
    return _clear_courier_data
