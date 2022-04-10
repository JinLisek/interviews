import re

from interview_2022_03_28.utility import AbstractSingletonMeta, log_err

from .order_validator import OrderValidator


class NullOrderValidator(OrderValidator, metaclass=AbstractSingletonMeta):
    def is_valid(self, order: str) -> bool:
        return True

    def set_next(self, validator: OrderValidator) -> OrderValidator:
        return validator


class BaseOrderValidator(OrderValidator):
    def __init__(self) -> None:
        OrderValidator.__init__(self)
        self._next: OrderValidator = NullOrderValidator()

    def set_next(self, validator: OrderValidator) -> OrderValidator:
        self._next = validator
        return self._next


class NumOfOrderFieldsValidator(BaseOrderValidator):
    def __init__(self, required_num_of_fields: int) -> None:
        BaseOrderValidator.__init__(self)
        self.__required_fields = required_num_of_fields
        self.__error_to_format = (
            "ERROR: Order should have at least {} fields, received: {}"
        )

    def is_valid(self, order: str) -> bool:
        split_order = order.split("|")

        if len(split_order) < self.__required_fields:
            log_err(self.__error_to_format.format(self.__required_fields, order))
            return False

        return self._next.is_valid(order=order)


class ActionValidator(BaseOrderValidator):
    def is_valid(self, order: str) -> bool:
        split_order = order.split("|")
        action = split_order[2]

        if action not in ("a", "u", "c"):
            log_err(f"ERROR: Cannot process order, unknown action: {action}")
            return False

        return self._next.is_valid(order=order)


class TimestampValidator(BaseOrderValidator):
    def is_valid(self, order: str) -> bool:
        split_order = order.split("|")
        timestamp = split_order[0]

        if not timestamp.isdigit():
            log_err(
                f"ERROR: Timestamp should be a unit unixstamp, received: {timestamp}"
            )
            return False

        return self._next.is_valid(order=order)


class OrderIdValidator(BaseOrderValidator):
    def __init__(self) -> None:
        BaseOrderValidator.__init__(self)
        self.__order_id_regex = re.compile("^[a-zA-Z0-9]+$")

    def is_valid(self, order: str) -> bool:
        split_order = order.split("|")
        order_id = split_order[1]

        if not self.__order_id_regex.match(order_id):
            log_err(f"ERROR: Format of order id is incorrect, received: {order_id}")
            return False

        return self._next.is_valid(order=order)


class SizeValidator(BaseOrderValidator):
    def __init__(self, size_idx: int) -> None:
        BaseOrderValidator.__init__(self)
        self.__size_idx = size_idx

    def is_valid(self, order: str) -> bool:
        split_order = order.split("|")
        size = split_order[self.__size_idx]

        if not size.isdigit():
            log_err(f"ERROR: Size should be a number, received: {size}")
            return False

        if int(size) < 1:
            log_err(f"ERROR: Size should be positive, received: {size}")
            return False

        return self._next.is_valid(order=order)


class SideValidator(BaseOrderValidator):
    def is_valid(self, order: str) -> bool:
        split_order = order.split("|")
        side = split_order[4]

        if side not in ("B", "S"):
            log_err(f"ERROR: Unknown transaction side: {side}, not processing order!")
            return False

        return self._next.is_valid(order=order)
