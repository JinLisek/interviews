import math
from typing import Dict

from .best_bid_and_ask_view import BestBidAndAskView
from .order import Order, OrderType
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
        self.left = None
        self.right = None
        self.price = order.price

        self.orders = {}
        self.orders[order.order_id] = order


class RedBlackTree:
    def __init__(self) -> None:
        self.root = None

    def insert(self, order: Order) -> None:
        new_node = RedBlackNode(order=order)
        new_node.red = True

        parent = None
        current = self.root
        while current is not None:
            parent = current
            if new_node.price < current.price:
                current = current.left
            elif new_node.price > current.price:
                current = current.right
            else:
                current.orders[order.order_id] = order
                return

        new_node.parent = parent
        if parent is None:
            self.root = new_node
        elif new_node.price < parent.price:
            parent.left = new_node
        else:
            parent.right = new_node

    def update(self, order: Order) -> None:
        node_to_remove = find(root=self.root, price=order.price)
        if node_to_remove is None:
            raise RuntimeError(f"BLAX NODE NOT FOUND TO UPDATE price {order.price}")

        node_to_remove.orders[order.order_id].size = order.size

    def remove(self, order: Order) -> None:
        node_to_remove = find(root=self.root, price=order.price)
        if node_to_remove is None:
            raise RuntimeError(f"BLAX NODE NOT FOUND TO REMOVE price {order.price}")

        if len(node_to_remove.orders) > 1:
            del node_to_remove.orders[order.order_id]
            return

        # original_is_red = node_to_remove.red

        if node_to_remove.left is None:
            # right_child = node_to_remove.right
            self.__transplant(parent=node_to_remove, child=node_to_remove.right)
        elif node_to_remove.right is None:
            self.__transplant(parent=node_to_remove, child=node_to_remove.left)
        else:
            minimal_right = minimal_node(root=node_to_remove.right)
            # minimal_right color
            right_child_of_minimal_right = minimal_right.right
            if minimal_right.parent is node_to_remove:
                right_child_of_minimal_right.parent = minimal_right
            else:
                self.__transplant(parent=minimal_right, child=minimal_right.right)
                minimal_right.right = node_to_remove.right
                minimal_right.right.parent = minimal_right

            self.__transplant(parent=node_to_remove, child=minimal_right)
            minimal_right.left = node_to_remove.left
            minimal_right.left.parent = minimal_right
            minimal_right.red = node_to_remove.red

    def get_minimum(self) -> float:
        min_node = minimal_node(root=self.root)

        if min_node is None:
            return 0.0

        return min_node.price

    def get_maximum(self) -> float:
        max_node = maximal_node(root=self.root)

        if max_node is None:
            return 0.0

        return max_node.price

    def __transplant(self, parent, child):
        if parent.parent is None:
            self.root = child
        elif parent is parent.parent.left:
            parent.parent.left = child
        else:
            parent.parent.right = child

        if child is not None:
            child.parent = parent.parent


def find(root, price: float) -> RedBlackNode:
    if root is None or math.isclose(root.price, price):
        return root

    if root.price < price:
        return find(root=root.right, price=price)

    return find(root=root.left, price=price)


def minimal_node(root) -> RedBlackNode:
    if root is None:
        return None

    current = root
    while current.left is not None:
        current = current.left

    return current


def maximal_node(root) -> RedBlackNode:
    if root is None:
        return None

    current = root
    while current.right is not None:
        current = current.right

    return current


TickerToOrders = Dict[str, Dict[str, RedBlackTree]]


class TreeOrderBook(OrderBookProcessor, BestBidAndAskView):
    def __init__(self) -> None:
        self.__orders: TickerToOrders = {}
        self.__ids_to_orders = {}

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
        self.__orders[order.ticker][container_name].remove(order=order)

    def get_best_ask(self, ticker: str) -> float:
        if ticker not in self.__orders:
            return 0.0
        return self.__orders[ticker]["asks"].get_minimum()

    def get_best_bid(self, ticker: str) -> float:
        if ticker not in self.__orders:
            return 0.0
        return self.__orders[ticker]["bids"].get_maximum()

    @property
    def orders(self) -> TickerToOrders:
        return self.__orders


def _container_from_order_type(order_type: OrderType) -> str:
    return "asks" if order_type == OrderType.ASK else "bids"
