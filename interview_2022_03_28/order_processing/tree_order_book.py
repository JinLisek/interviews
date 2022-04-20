from typing import Dict, Tuple

from .best_bid_and_ask_view import BestBidAndAskView
from .order import Order
from .order_book import OrderBookError, OrderBookProcessor


class OrderDoesNotExistError(OrderBookError):
    pass


class InvalidOrderSizeZeroError(OrderBookError):
    pass


class DuplicatedOrderIdError(OrderBookError):
    pass


class RedBlackNode:
    def __init__(self, order: Order) -> None:
        self.red = False
        self.parent = None
        self.order = order
        self.left = None
        self.right = None


class RedBlackTree:
    def __init__(self) -> None:
        self.root = None

    def insert(self, order: Order) -> None:
        new_node = RedBlackNode(order=order)
        new_node.red = True

        parent = None
        current = self.root
        while current != None:
            parent = current
            if new_node.order.price < current.order.price:
                current = current.left
            elif new_node.order.price > current.order.price:
                current = current.right
            else:
                return  # duplicates should be handled better

        new_node.parent = parent
        if parent == None:
            self.root = new_node
        elif new_node.order.price < parent.order.price:
            parent.left = new_node
        else:
            parent.right = new_node

    def remove(self, order: Order) -> None:
        current = self.root

        while current != None:
            if order.price < current.order.price:
                current = current.left
            elif order.price > current.order.price:
                current = current.right
            else:
                # delete order
                pass

    def get_minimum(self) -> float:
        if self.root == None:
            return 0

        current = self.root
        while current.left is not None:
            current = current.left

        return current.order.price


TickerToOrders = Dict[str, Dict[str, RedBlackTree]]


class TreeOrderBook(OrderBookProcessor):
    def __init__(self) -> None:
        self.__orders: TickerToOrders = {}
        self.__order_id_to_order = {}
        self.__order_ids = set()

    def add_order(self, order: Order) -> None:
        if order.size == 0:
            raise InvalidOrderSizeZeroError(
                f"Cannot add order with id: {order.order_id} due to size being 0."
            )

        if order.order_id in self.__order_ids:
            raise DuplicatedOrderIdError(
                f"Cannot add order with id: {order.order_id} to book."
            )

        if order.ticker not in self.__orders:
            self.__orders[order.ticker] = {}
            self.__orders[order.ticker]["asks"] = RedBlackTree()
            self.__orders[order.ticker]["bids"] = RedBlackTree()

        self.__order_id_to_order[order.order_id] = order
        self.__orders[order.ticker]["asks"].insert(order=order)
        self.__order_ids.add(order.order_id)

    def update(self, order_id: str, size: int) -> None:
        pass

    def cancel(self, order_id: str) -> None:
        order = self.__order_id_to_order[order_id]
        self.__asks[order.ticker].remove(order=order)

    def get_best_ask(self, ticker: str) -> float:
        if ticker not in self.__asks:
            return 0
        return self.__asks[ticker].get_minimum()

    @property
    def orders(self) -> TickerToOrders:
        return self.__orders
