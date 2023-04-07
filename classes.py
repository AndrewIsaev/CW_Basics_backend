import marshmallow
import marshmallow_dataclass
from datetime import datetime
from dataclasses import dataclass, field


@dataclass
class Currency:
    name: str
    code: str

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class OperationAmount:
    amount: str
    currency: Currency

    class Meta:
        unknown = marshmallow.EXCLUDE


@dataclass
class Operation:
    id: int
    date: str
    state: str
    operation_amount: OperationAmount = field(metadata={"data_key": "operationAmount"})
    description: str
    from_: str | None = field(metadata={"data_key": "from"})
    to: str

    class Meta:
        unknown = marshmallow.EXCLUDE

    def __repr__(self):
        if self.from_:
            return f"{self._dmy_date} {self.description}\n" \
                   f"{self._hide_from} -> {self._hide_to}\n" \
                   f"{self.operation_amount.amount} {self.operation_amount.currency.name}\n"
        else:
            return f"{self._dmy_date} {self.description}\n" \
                   f"{self._hide_to}\n" \
                   f"{self.operation_amount.amount} {self.operation_amount.currency.name}\n"

    def _is_card(self, message: str) -> bool:
        """
        Check number of account
        :param message: from or to message
        :return: False if message contains "счет" else True
        """
        if "счет" in self._get_account_name(message).lower():
            return False
        return True

    @property
    def _dmy_date(self) -> str:
        self.date = datetime.strptime(self.date, "%Y-%m-%dT%H:%M:%S.%f").date()
        return datetime.strftime(self.date, "%d.%m.%Y")

    def _get_account_number(self, message: str) -> str:
        """
        Get account number from or to message
        :param message:
        :return:
        """
        if message:
            if self._is_card(message):
                number = message.split()[-1]
                card_number = f"{number[:4]} {number[4:8]} {number[8:12]} {number[-4:]}"
                to_change = card_number[7:-4]
                return card_number.replace(to_change, "** **** ")
            else:
                return f"**{message.split()[-1][-4:]}"
        return ""

    @staticmethod
    def _get_account_name(message: str) -> str:
        """
        Get account number from or to message
        :param message:
        :return:
        """
        if message:
            return " ".join(message.split()[:-1])
        return ""

    @property
    def _hide_from(self) -> str:
        return f"{self._get_account_name(self.from_)} {self._get_account_number(self.from_)}"

    @property
    def _hide_to(self) -> str:
        return f"{self._get_account_name(self.to)} {self._get_account_number(self.to)}"


OperationSchema = marshmallow_dataclass.class_schema(Operation)
