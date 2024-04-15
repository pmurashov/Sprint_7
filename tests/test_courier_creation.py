# -*- coding: utf-8 -*-

import allure
from utils.helpers import register_new_courier_and_return_login_password
from utils.constants import COURIER_NAME, COURIER_PASSWORD, COURIER_LOGIN


@allure.story("Создание курьеров")
class TestCourierCreation:
    @allure.title("Курьера можно создать")
    def test_create_courier_answer_correct_response_code(self, api_client, clear_courier_data):
        courier_info = register_new_courier_and_return_login_password()
        login, password, first_name = courier_info[0][:-1], courier_info[1], courier_info[2]
        response = api_client.create_courier(login, password, first_name)
        assert response.status_code == 201 and response.json()["ok"] == True, "Код ответа должен быть 201, ok: True"
        clear_courier_data(api_client, login, password)

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_courier_double(self, api_client, clear_courier_data):
        expected_message = "Этот логин уже используется. Попробуйте другой."
        courier_info = register_new_courier_and_return_login_password()
        login, password, first_name = courier_info[0], courier_info[1], courier_info[2]

        api_client.create_courier(login, password, first_name)
        response = api_client.create_courier(login, password, first_name)

        assert response.status_code == 409 and expected_message in response.json()["message"]
        clear_courier_data(api_client, login, password)

    @allure.title("Чтобы создать курьера, нужно передать в ручку все обязательные поля")
    def test_create_courier_missing_login(self, api_client):
        expected_message = "Недостаточно данных для создания учетной записи"
        payload = {
            "login": "jinja"
        }
        response = api_client.create_courier_without_login_or_password(payload)
        assert response.status_code == 400 and expected_message in response.json()["message"]

    @allure.title("Если создать пользователя с логином, который уже есть, возвращается ошибка")
    def test_create_existing_login_courier_error(self, api_client):
        expected_error_message = "Этот логин уже используется. Попробуйте другой."
        response = api_client.create_courier(COURIER_LOGIN, COURIER_PASSWORD, COURIER_NAME)
        assert response.status_code == 409 and response.json()["message"] == expected_error_message
