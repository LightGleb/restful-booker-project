import allure

from restful_booker.utils.request_helper import api_request
from tests.conftest import create_token


@allure.parent_suite('API')
@allure.suite('Бронирование')
@allure.title(f"Удаление бронирования")
@allure.severity('Critical')
def test_delete_booking(get_booking_id):
    endpoint = '/booking/' + get_booking_id

    headers = {
        'Cookie': 'token=' + create_token(),
        'Content-Type': 'application/json'
    }

    with allure.step('Выполняем запрос на удаление бронирования'):
        response = api_request(endpoint, method="DELETE", headers=headers)
    with allure.step('Проверяем статус код ответа'):
        assert response.status_code == 201
    with allure.step('Проверяем что бронирование удалилось'):
        response = api_request(endpoint, method="GET")
        assert response.status_code == 404
