import allure
from utils.constants import ORDER_REQUIRED_FIELDS


@allure.story("Проверка списка заказов")
class TestOrderList:
    @allure.title("Проверка наличия всех необходимых полей в заказах")
    def test_get_orders_all_required_fields_absent(self, api_client):
        response = api_client.get_orders()
        orders = response.json().get("orders", [])
        missing_fields = [field for field in ORDER_REQUIRED_FIELDS if field not in orders[0]]
        assert not missing_fields, f"Следующие поля не найдены: {missing_fields}"
