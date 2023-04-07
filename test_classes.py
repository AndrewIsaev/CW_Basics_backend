from datetime import datetime

import pytest

from classes import Operation, OperationSchema


@pytest.fixture
def operation(raw_data):
    return OperationSchema().load(data=raw_data)


@pytest.fixture
def raw_data():
    return {
        "id": 957763565,
        "state": "EXECUTED",
        "date": "2019-01-05T00:52:30.108534",
        "operationAmount": {
            "amount": "87941.37",
            "currency": {
                "name": "руб.",
                "code": "RUB"
            }
        },
        "description": "Перевод со счета на счет",
        "from": "Счет 46363668439560358409",
        "to": "Счет 18889008294666828266"
    }


class TestClass:
    def test__is_card(self, operation):
        assert operation._is_card("Visa 46363668439560358409") == True
        assert operation._is_card("Счет 18889008294666828266") == False

    def test__dmy_date(self, operation):
        assert operation._dmy_date == "05.01.2019"

    def test__get_account_number(self, operation):
        assert operation._get_account_number("Счет 46363668439560358409") == "**8409"
        assert operation._get_account_number("МИР 5211277418228469") == "5211 27** **** 8469"
        assert operation._get_account_number(None) == ""

    def test__get_account_name(self, operation):
        assert operation._get_account_name("Счет 46363668439560358409") == "Счет"
        assert operation._get_account_name("МИР 5211277418228469") == "МИР"
        assert operation._get_account_name("Visa Gold 5211277418228469") == "Visa Gold"
        assert operation._get_account_name(None) == ""
