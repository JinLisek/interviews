from ._concrete_validators import (
    ActionValidator,
    NumOfOrderFieldsValidator,
    OrderIdValidator,
    SideValidator,
    SizeValidator,
    TimestampValidator,
)
from .order_validator import OrderValidator


def create_action_validator() -> OrderValidator:
    validator = NumOfOrderFieldsValidator(required_num_of_fields=3)
    validator.set_next(validator=ActionValidator())
    return validator


def create_cancel_validator() -> OrderValidator:
    num_validator = NumOfOrderFieldsValidator(required_num_of_fields=3)
    timestamp_validator = TimestampValidator()

    num_validator.set_next(validator=timestamp_validator)
    timestamp_validator.set_next(validator=OrderIdValidator())

    return num_validator


def create_update_validator() -> OrderValidator:
    num_validator = NumOfOrderFieldsValidator(required_num_of_fields=4)
    timestamp_validator = TimestampValidator()
    order_id_validator = OrderIdValidator()

    num_validator.set_next(validator=timestamp_validator)
    timestamp_validator.set_next(validator=order_id_validator)
    order_id_validator.set_next(validator=SizeValidator(size_idx=3))

    return num_validator


def create_add_validator() -> OrderValidator:
    num_validator = NumOfOrderFieldsValidator(required_num_of_fields=7)
    timestamp_validator = TimestampValidator()
    order_id_validator = OrderIdValidator()
    side_validator = SideValidator()

    num_validator.set_next(validator=timestamp_validator)
    timestamp_validator.set_next(validator=order_id_validator)
    order_id_validator.set_next(validator=side_validator)
    side_validator.set_next(validator=SizeValidator(size_idx=6))

    return num_validator
