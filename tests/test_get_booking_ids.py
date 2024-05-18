import allure

from restful_booker.utils.request_helper import api_request


@allure.parent_suite('API')
@allure.suite('Бронирование')
@allure.title(f"Получение ids бронирования")
@allure.severity('Major')
def test_get_booking_ids(get_booking_id):
    endpoint = '/booking/'
    with allure.step('Выполняем запрос на получение ids бронирования'):
        response = api_request(endpoint, method="GET")
    with allure.step('Проверяем статус код ответа'):
        assert response.status_code == 200
    with allure.step('Получаем id через параметры'):
        params = {'firstname': 'Super', 'lastname': 'Man'}
        response = api_request(endpoint, method="GET", params=params)
        body = response.json()
    with allure.step('Проверяем вхождение id'):
        assert get_booking_id in str(body)
