import os

from utils import load_data, filter_by_executed

DATA = os.path.join(".", "operations.json")

if __name__ == '__main__':
    # load operations from json
    all_operations = load_data(DATA)

    # filter by state
    executed_operations = filter_by_executed(all_operations)
    # sorted by date
    last_five_executed_operations = sorted(executed_operations, key=lambda x: x.date)[-5:]
    # display
    for operation in last_five_executed_operations:
        print(operation)
