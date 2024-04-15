import allure


@allure.story("Проверка списка заказов")
class TestOrderList:
    @allure.title("Проверка наличия всех необходимых полей в заказах")
    def test_get_orders_all_required_fields_absent(self, api_client):
        required_fields = ["id", "firstName", "lastName", "address", "metroStation", "phone",
                           "rentTime", "deliveryDate", "track", "color", "comment", "createdAt",
                           "updatedAt", "status"]
        response = api_client.get_orders()
        orders = response.json().get("orders", [])
        missing_fields = [field for field in required_fields if field not in orders[0]]
        assert not missing_fields, f"Следующие поля не найдены: {missing_fields}"
