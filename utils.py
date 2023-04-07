import json

from classes import OperationSchema


def load_data(data: str) -> list[dict]:
    """
    Load data from json file with operations
    :param data:
    :return: list with dicts of operations
    """
    with open(data, encoding="UTF-8") as file:
        return json.load(file)


def filter_by_executed(all_operations: list[dict]) -> list[dict]:
    """

    :param all_operations: list with all_operations
    :return: list with executed operations
    """
    executed_operations = []
    for item in all_operations:
        operation = OperationSchema().load(data=item)
        if operation.state == "EXECUTED":
            executed_operations.append(operation)
    return executed_operations
