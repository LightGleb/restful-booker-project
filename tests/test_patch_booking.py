import json

import allure
import requests
from jsonschema.validators import validate

from restful_booker.utils.attach import response_logging, response_attaching
from schemas.patch_booking import partial_update_booking
from tests.conftest import create_token, API_URL


@allure.parent_suite('API')
@allure.suite('Бронирование')
@allure.title(f"Частичное обновление бронирования")
@allure.severity('Major')
def test_patch_booking(get_booking_id):
    endpoint = '/booking/' + get_booking_id

    payload = json.dumps({
        "firstname": "James",
        "lastname": "Cameron"
    })
    headers = {
        'Cookie': 'token=' + create_token(),
        'Content-Type': 'application/json'
    }

    with allure.step('Выполняем запрос на обновление бронирования'):
        response = requests.patch(API_URL + endpoint, headers=headers, data=payload)
    with allure.step('Проверяем статус код ответа'):
        assert response.status_code == 200
    with allure.step('Проверяем соответствие схеме'):
        body = response.json()
        validate(body, partial_update_booking)
    with allure.step('Сверяем обновлённые данные'):
        body = response.json()
        payload_dict = json.loads(payload)
        assert payload_dict["firstname"] == body["firstname"]
        assert payload_dict["lastname"] == body["lastname"]
    response_logging(response)
    response_attaching(response)