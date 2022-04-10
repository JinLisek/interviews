from interview_2022_03_28.utility import log_err

from . import validators
from .order import Order, OrderType
from .order_book import OrderBookError, OrderBookProcessor

ACTION_VALIDATOR = validators.create_action_validator()
CANCEL_VALIDATOR = validators.create_cancel_validator()
UPDATE_VALIDATOR = validators.create_update_validator()
ADD_VALIDATOR = validators.create_add_validator()


def process_order(order_book: OrderBookProcessor, order: str) -> None:
    if not ACTION_VALIDATOR.is_valid(order=order):
        return

    order_fields = order.split("|")
    action = order_fields[2]

    if action == "c":
        _handle_cancel_action(order_book=order_book, order=order)

    if action == "u":
        _handle_update_action(order_book=order_book, order=order)

    if action == "a":
        _handle_add_action(order_book=order_book, order=order)


def _handle_cancel_action(order_book: OrderBookProcessor, order: str) -> None:
    if not CANCEL_VALIDATOR.is_valid(order=order):
        return

    order_fields = order.split("|")
    order_id = order_fields[1]

    try:
        order_book.cancel(order_id=order_id)
    except OrderBookError as err:
        log_err("ERROR: " + str(err))


def _handle_update_action(order_book: OrderBookProcessor, order: str) -> None:
    if not UPDATE_VALIDATOR.is_valid(order=order):
        return

    order_fields = order.split("|")
    order_id = order_fields[1]
    size = int(order_fields[3])

    try:
        order_book.update(order_id=order_id, size=size)
    except OrderBookError as err:
        log_err("ERROR: " + str(err))


def _handle_add_action(order_book: OrderBookProcessor, order: str) -> None:
    if not ADD_VALIDATOR.is_valid(order=order):
        return

    order_fields = order.split("|")
    timestamp, order_id, _, ticker, side, price, size = order_fields

    order_type = OrderType.BID if side == "B" else OrderType.ASK

    new_order = Order(
        order_id=order_id,
        timestamp=timestamp,
        ticker=ticker,
        price=float(price),
        size=int(size),
        order_type=order_type,
    )

    try:
        order_book.add_order(order=new_order)
    except OrderBookError as err:
        log_err("ERROR: " + str(err))
