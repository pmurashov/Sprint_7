# -*- coding: utf-8 -*-

import allure
from utils.helpers import register_new_courier_and_return_login_password
from utils.constants import COURIER_LOGIN, COURIER_PASSWORD


@allure.story("Проверка авторизации курьеров")
class TestCourierLogin:
    @allure.title("Курьер может авторизоваться")
    def test_courier_login_successfully(self, api_client):
        courier_info = register_new_courier_and_return_login_password()
        login, password, first_name = courier_info[0], courier_info[1], courier_info[2]
        response = api_client.courier_login(login, password)
        assert response.status_code == 200 and "id" in response.json()
        api_client.delete_courier(response.json()["id"])

    @allure.title("Система вернёт ошибку, если неправильно указать логин")
    def test_courier_login_error_login(self, api_client):
        expected_error_message = "Учетная запись не найдена"
        response = api_client.courier_login(COURIER_LOGIN + "wrong login for sure", COURIER_PASSWORD)
        assert response.status_code == 404 and response.json()["message"] == expected_error_message

    @allure.title("Система вернёт ошибку, если неправильно указать пароль")
    def test_courier_login_error_password(self, api_client):
        expected_error_message = "Учетная запись не найдена"
        response = api_client.courier_login(COURIER_LOGIN, "wrong password")
        assert response.status_code == 404 and response.json()["message"] == expected_error_message

    @allure.title("Запрос возвращает ошибку, если неправильно указать логин")
    def test_courier_login_missing_login(self, api_client):
        response = api_client.courier_login("", COURIER_PASSWORD)
        expected_error_message = "Недостаточно данных для входа"
        assert response.status_code == 400 and response.json()["message"] == expected_error_message

    @allure.title("Запрос возвращает ошибку, если неправильно указать пароль")
    def test_courier_login_missing_password(self, api_client):
        response = api_client.courier_login(COURIER_LOGIN, "")
        expected_error_message = "Недостаточно данных для входа"
        assert response.status_code == 400 and response.json()["message"] == expected_error_message
