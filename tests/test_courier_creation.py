import allure
from utils.constants import COURIER_NAME, COURIER_PASSWORD, COURIER_LOGIN, MESSAGE_LOGIN_ALREADY_USED, \
    MESSAGE_NOT_ENOUGH_CREATE_DATA
from utils.helpers import register_new_courier_and_return_login_password


@allure.story("Создание курьеров")
class TestCourierCreation:
    @allure.title("Курьера можно создать")
    def test_create_courier_answer_correct_response_code(self, api_client, clear_courier_data):
        courier_info = register_new_courier_and_return_login_password()
        login, password, first_name = courier_info[0][:-1], courier_info[1], courier_info[2]
        response = api_client.create_courier(login, password, first_name)
        clear_courier_data(api_client, login, password)
        assert response.status_code == 201 and response.json()["ok"] == True, "Код ответа должен быть 201, ok: True"

    @allure.title("Нельзя создать двух одинаковых курьеров")
    def test_create_courier_double(self, api_client, clear_courier_data):
        courier_info = register_new_courier_and_return_login_password()
        login, password, first_name = courier_info[0], courier_info[1], courier_info[2]

        api_client.create_courier(login, password, first_name)
        response = api_client.create_courier(login, password, first_name)
        clear_courier_data(api_client, login, password)

        assert response.status_code == 409 and MESSAGE_LOGIN_ALREADY_USED in response.json()["message"]

    @allure.title("Чтобы создать курьера, нужно передать в ручку все обязательные поля")
    def test_create_courier_missing_login(self, api_client):
        response = api_client.create_courier_without_password("jinja")
        assert response.status_code == 400 and MESSAGE_NOT_ENOUGH_CREATE_DATA in response.json()["message"]

    @allure.title("Если создать пользователя с логином, который уже есть, возвращается ошибка")
    def test_create_existing_login_courier_error(self, api_client):
        response = api_client.create_courier(COURIER_LOGIN, COURIER_PASSWORD, COURIER_NAME)
        assert response.status_code == 409 and response.json()["message"] == MESSAGE_LOGIN_ALREADY_USED
