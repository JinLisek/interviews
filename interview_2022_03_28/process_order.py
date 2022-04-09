from .logger import log_err
from .order import Order, OrderType
from .order_book import DatabaseOrderBook, OrderBookError

KNOWN_ACTIONS = ("a", "u", "c")


def process_order(order_book: DatabaseOrderBook, order: str) -> None:
    order_data = order.split("|")
    if len(order_data) < 3:
        log_err(f"ERROR: Order should have at least 3 fields, received: {order}")
        return
    order_id = order_data[1]
    action = order_data[2]

    if action not in KNOWN_ACTIONS:
        log_err(f"ERROR: Cannot process order, unknown action: {action}")

    if action == "c":
        try:
            order_book.cancel(order_id=order_id)
        except OrderBookError as err:
            log_err("ERROR: " + str(err))
        return

    if action == "u":
        if len(order_data) < 4:
            log_err(f"ERROR: Update should have at least 4 fields, received: {order}")
            return
        size = order_data[3]
        if not size.isdigit() or int(size) < 1:
            log_err(f"ERROR: Size should be a positive integer, received size: {size}")
            return
        try:
            order_book.update(order_id=order_id, size=int(size))
        except OrderBookError as err:
            log_err("ERROR: " + str(err))
        return

    if action == "a":
        timestamp, order_id, action, ticker, side, price, size = order_data

        if not size.isdigit() or int(size) < 1:
            log_err(f"ERROR: Size should be a positive integer, received size: {size}")
            return

        if side not in ["B", "S"]:
            log_err(f"ERROR: Unknown transaction side: {side}, not processing order!")
            return

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
