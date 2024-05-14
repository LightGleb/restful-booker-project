import allure
import requests

from restful_booker.utils.attach import response_logging, response_attaching
from tests.conftest import create_token, API_URL


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
        response = requests.delete(API_URL + endpoint, headers=headers)
    with allure.step('Проверяем статус код ответа'):
        assert response.status_code == 201
    with allure.step('Проверяем что бронирование удалилось'):
        response = requests.get(API_URL + endpoint)
        assert response.status_code == 404

    response_logging(response)
    response_attaching(response)
