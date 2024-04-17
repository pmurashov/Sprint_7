import allure
import pytest


@allure.story("Проверка создания заказов")
class TestOrderCreation:
    @pytest.mark.parametrize("color", [["BLACK"], ["GREY"], ["BLACK", "GREY"], []])
    @allure.title("Создание заказа")
    def test_create_order(self, api_client, color):
        order_data = {
            "firstName": "Pavel",
            "lastName": "Murashov",
            "address": "Moscow, Poltavskaya 2",
            "metroStation": 159,
            "phone": "+7 333 522 77 69",
            "rentTime": 2,
            "deliveryDate": "2024-04-08",
            "comment": "No comment",
            "color": color
        }

        with allure.step(f"Создание заказа с цветом {color}"):
            response = api_client.create_order(order_data)
            assert response.status_code == 201 and "track" in response.json(), "Код ответа должен быть 201, в теле ответа должно быть поле track"
