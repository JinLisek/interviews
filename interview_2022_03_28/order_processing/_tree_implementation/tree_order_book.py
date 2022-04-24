from typing import Dict

from ..best_bid_and_ask_view import BestBidAndAskView
from ..order import Order, OrderType
from ..order_book import OrderBookError, OrderBookProcessor
from .red_black_tree import RedBlackTree


class OrderDoesNotExistError(OrderBookError):
    pass


class InvalidOrderSizeZeroError(OrderBookError):
    pass


class DuplicatedOrderIdError(OrderBookError):
    pass


TickerOrders = Dict[str, Dict[str, RedBlackTree]]


class TreeOrderBook(OrderBookProcessor, BestBidAndAskView):
    def __init__(self) -> None:
        self.__orders: TickerOrders = {}
        self.__ids_to_orders: Dict[str, Order] = {}

    def add_order(self, order: Order) -> None:
        if order.size == 0:
            raise InvalidOrderSizeZeroError(
                f"Cannot add order with id: {order.order_id} due to size being 0."
            )

        if order.order_id in self.__ids_to_orders:
            raise DuplicatedOrderIdError(
                f"Cannot add order with id: {order.order_id} to book."
            )

        if order.ticker not in self.__orders:
            self.__orders[order.ticker] = {}
            self.__orders[order.ticker]["asks"] = RedBlackTree()
            self.__orders[order.ticker]["bids"] = RedBlackTree()

        container_name = _container_from_order_type(order_type=order.order_type)
        self.__orders[order.ticker][container_name].insert(order=order)
        self.__ids_to_orders[order.order_id] = order

    def update(self, order_id: str, size: int) -> None:
        if order_id not in self.__ids_to_orders:
            raise OrderDoesNotExistError(
                f"Cannot update non existing order: {order_id}"
            )

        order = self.__ids_to_orders[order_id]
        order.size = size
        container_name = _container_from_order_type(order_type=order.order_type)
        self.__orders[order.ticker][container_name].update(order=order)

    def cancel(self, order_id: str) -> None:
        if order_id not in self.__ids_to_orders:
            raise OrderDoesNotExistError(
                f"Cannot cancel non existing order: {order_id}"
            )

        order = self.__ids_to_orders[order_id]
        container_name = _container_from_order_type(order_type=order.order_type)
        self.__orders[order.ticker][container_name].delete(order=order)

    def get_best_ask(self, ticker: str) -> float:
        if ticker not in self.__orders:
            return 0.0
        return self.__orders[ticker]["asks"].get_minimum()

    def get_best_bid(self, ticker: str) -> float:
        if ticker not in self.__orders:
            return 0.0
        return self.__orders[ticker]["bids"].get_maximum()

    @property
    def orders(self) -> TickerOrders:
        return self.__orders


def _container_from_order_type(order_type: OrderType) -> str:
    return "asks" if order_type == OrderType.ASK else "bids"
