import os

import requests
from allure_commons._allure import step
from dotenv import load_dotenv

import json
import logging
import allure

from requests import Response
from allure_commons.types import AttachmentType

load_dotenv()

API_URL = os.getenv('API_URL')


def api_request(endpoint, method, **kwargs):
    with step("API Request"):
        response = requests.request(method, url=f"https://{API_URL}{endpoint}", **kwargs)
        response_logging(response)
        response_attaching(response)
    return response


def response_logging(response: Response):
    logging.info("Request: " + response.request.url)
    if response.request.body:
        logging.info("INFO Request body: " + response.request.body)
    logging.info("Request headers: " + str(response.request.headers))
    logging.info("Response code " + str(response.status_code))
    logging.info("Response: " + response.text)


def response_attaching(response: Response):
    allure.attach(
        body=response.request.url,
        name="Request url",
        attachment_type=AttachmentType.TEXT,
    )
    if str(response.content):
        allure.attach(
            body=response.content,
            name="Response",
            attachment_type=AttachmentType.TEXT,
        )
    else:
        allure.attach(
            body=json.dumps(response.json(), indent=4, ensure_ascii=True),
            name="Response",
            attachment_type=AttachmentType.JSON,
            extension="json",
        )
    if response.request.body:
        allure.attach(
            body=json.dumps(response.request.body, indent=4, ensure_ascii=True),
            name="Request body",
            attachment_type=AttachmentType.JSON,
            extension="json",
        )
