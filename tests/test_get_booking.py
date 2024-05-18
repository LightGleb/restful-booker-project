import allure
from jsonschema.validators import validate

from restful_booker.utils.request_helper import api_request
from schemas.get_booking import booking


@allure.parent_suite('API')
@allure.suite('Бронирование')
@allure.title(f"Получение бронирования")
@allure.severity('Major')
def test_get_booking(get_booking_id):
    endpoint = '/booking/' + get_booking_id
    with allure.step('Выполняем запрос на получение бронирования'):
        response = api_request(endpoint, method="GET")
    with allure.step('Проверяем статус код ответа'):
        assert response.status_code == 200
    with allure.step('Проверяем соответствие схеме'):
        body = response.json()
        validate(body, booking)
    with allure.step('Проверяем выплату депозита'):
        assert body["depositpaid"] is True
