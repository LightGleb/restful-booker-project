import json
import os

import allure
import pytest
import requests
from dotenv import load_dotenv

from jsonschema.validators import validate

from restful_booker.utils.attach import response_logging, response_attaching
from schemas.post_booking import new_booking

load_dotenv()

API_URL = os.getenv('API_URL')


def create_token():
    endpoint = "/auth"

    payload = json.dumps({
        "username": os.getenv('USER_NAME'),
        "password": os.getenv('PASSWORD')
    })
    headers = {
        'Content-Type': 'application/json'
    }

    with allure.step('Создаём токен'):
        response = requests.post(API_URL + endpoint, headers=headers, data=payload)

    with allure.step('Проверяем статус код ответа'):
        assert response.status_code == 200

    body = response.json()

    token = body["token"]

    return token


@pytest.fixture(scope='function')
def get_booking_id():
    endpoint = '/booking/'

    headers = {
        'Content-Type': 'application/json'
    }

    payload = json.dumps({
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    })

    with allure.step('Выполняем запрос на создание бронирования'):
        response = requests.post(API_URL + endpoint, headers=headers, data=payload)

    with allure.step('Проверяем статус код ответа'):
        assert response.status_code == 200

    with allure.step('Проверяем соответствие схеме'):
        body = response.json()
        validate(body, new_booking)

    with allure.step('Сверяем имя на кого оформлена бронь'):
        payload_dict = json.loads(payload)
        assert payload_dict["firstname"] == body["booking"]["firstname"]

    booking_id = str(body["bookingid"])

    response_logging(response)
    response_attaching(response)

    return booking_id
