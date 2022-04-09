from .concrete_order_database import OrderDatabase
from .order import Order, OrderType


class OrderBookError(Exception):
    pass


class OrderDoesNotExistError(OrderBookError):
    pass


class InvalidOrderSizeZeroError(OrderBookError):
    pass


class DuplicatedOrderIdError(OrderBookError):
    pass


class DatabaseOrderBook:
    def __init__(self, database: OrderDatabase) -> None:
        self.__database = database

        order_types = ", ".join(
            [f"'{order_type.name}'" for order_type in list(OrderType)]
        )

        self.__database.create_table(
            name="orders",
            columns={
                "order_id": "text primary key not null",
                "time_created": "timestamp not null",
                "ticker": "text not null",
                "price": "real not null",
                "size": "integer not null",
                "type": f"text check(type in ({order_types})) not null",
            },
        )

    def add_order(self, order: Order) -> None:
        if order.size == 0:
            raise InvalidOrderSizeZeroError(
                f"Cannot add order with id: {order.order_id} due to size being 0."
            )

        try:
            self.__database.insert(order=order)
        except Exception as err:
            raise DuplicatedOrderIdError(
                f"Cannot add order with id: {order.order_id} to database." + str(err)
            ) from err

    def get_best_ask(self, ticker: str) -> float:
        return self.__database.get_best_ask(ticker=ticker)

    def get_best_bid(self, ticker: str) -> float:
        return self.__database.get_best_bid(ticker=ticker)

    def cancel(self, order_id: str) -> None:
        if not self.__database.has_order(order_id=order_id):
            raise OrderDoesNotExistError(
                f"Cannot cancel non existing order: {order_id}"
            )
        self.__database.remove(order_id=order_id)

    def update(self, order_id: str, size: int) -> None:
        if not self.__database.has_order(order_id=order_id):
            raise OrderDoesNotExistError(
                f"Cannot update non existing order: {order_id}"
            )
        self.__database.update(order_id=order_id, size=size)
