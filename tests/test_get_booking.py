import allure
import requests
from jsonschema.validators import validate

from restful_booker.utils.attach import response_logging, response_attaching
from schemas.get_booking import booking
from tests.conftest import API_URL


@allure.parent_suite('API')
@allure.suite('Бронирование')
@allure.title(f"Получение бронирования")
@allure.severity('Major')
def test_get_booking(get_booking_id):
    endpoint = '/booking/' + get_booking_id
    with allure.step('Выполняем запрос на получение бронирования'):
        response = requests.get(API_URL + endpoint)
    with allure.step('Проверяем статус код ответа'):
        assert response.status_code == 200
    with allure.step('Проверяем соответствие схеме'):
        body = response.json()
        validate(body, booking)
    with allure.step('Проверяем выплату депозита'):
        assert body["depositpaid"] is True
    response_logging(response)
    response_attaching(response)
