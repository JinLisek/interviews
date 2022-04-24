from __future__ import annotations

import math
from enum import Enum, auto, unique
from typing import Dict, Optional

from ..best_bid_and_ask_view import BestBidAndAskView
from ..order import Order, OrderType
from ..order_book import OrderBookError, OrderBookProcessor


class OrderDoesNotExistError(OrderBookError):
    pass


class InvalidOrderSizeZeroError(OrderBookError):
    pass


class DuplicatedOrderIdError(OrderBookError):
    pass


@unique
class NodeColor(Enum):
    RED = auto()
    BLACK = auto()


class RedBlackNode:
    def __init__(self, order: Order, parent: Optional[RedBlackNode]) -> None:
        self.color: NodeColor = NodeColor.RED
        self.parent: Optional[RedBlackNode] = parent
        self.left: Optional[RedBlackNode] = None
        self.right: Optional[RedBlackNode] = None
        self.price = order.price

        self.orders = {}
        self.orders[order.order_id] = order


class RedBlackTree:
    def __init__(self) -> None:
        self.root: Optional[RedBlackNode] = None

    def insert(self, order: Order) -> None:
        parent: Optional[RedBlackNode] = None
        current = self.root

        # find parent for new node
        while current is not None:
            parent = current
            if order.price < current.price:
                current = current.left
            elif order.price > current.price:
                current = current.right
            else:
                current.orders[order.order_id] = order
                return

        current_node = RedBlackNode(order=order, parent=parent)

        if parent is None:
            self.root = current_node
            return

        # set new node as child to the parent
        while parent is not None:
            if current_node.price < parent.price:
                parent.left = current_node
            else:
                parent.right = current_node

            # loop?
            if parent.color == NodeColor.BLACK:
                # insertion case 1: parent is black
                return

            grandparent = parent.parent

            if grandparent is None:
                # insertion case 4: parent is red and root
                parent.color = NodeColor.BLACK
                return

            uncle = find_brother(node=parent)
            if uncle is None or uncle.color == NodeColor.BLACK:
                # insertion case 5 and 6: parent is red, uncle is black
                if uncle is grandparent.right and current_node is parent.right:
                    # insertion case 5: parent is red, uncle is black, current_node is right inner grandchild of grandparent
                    self.__rotate_left(parent=parent)
                    current_node = parent
                    parent = grandparent.left
                elif uncle is grandparent.left and current_node is parent.left:
                    # insertion case 5: parent is red, uncle is black, current_node is left inner grandchild of grandparent
                    self.__rotate_right(parent=parent)
                    current_node = parent
                    parent = grandparent.right

                # insertion case 6: parent is red, uncle is black, current_node is outer grandchild of grandparent
                if uncle is grandparent.right:
                    self.__rotate_right(parent=grandparent)
                else:
                    self.__rotate_left(parent=grandparent)
                parent.color = NodeColor.BLACK
                grandparent.color = NodeColor.RED

                return

            # insertion case 2: parent is red, uncle is red
            parent.color = NodeColor.BLACK
            uncle.color = NodeColor.BLACK
            grandparent.color = NodeColor.RED
            current_node = grandparent
            parent = current_node.parent

        # insertion case 3: current_node is root and red

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

    def __rotate_left(self, parent: RedBlackNode) -> RedBlackNode:
        grandparent = parent.parent
        new_subtree_root = parent.right
        if new_subtree_root is None:
            raise RuntimeError("NEW SUBTREE ROOT SHOULD BE TRUE NODE")

        child = new_subtree_root.left

        parent.right = child
        if child is not None:
            child.parent = parent

        new_subtree_root.left = parent
        parent.parent = new_subtree_root
        new_subtree_root.parent = grandparent

        if grandparent is not None:
            if grandparent.left is parent:
                grandparent.left = new_subtree_root
            else:
                grandparent.right = new_subtree_root
        else:
            self.root = new_subtree_root

        return new_subtree_root

    def __rotate_right(self, parent: RedBlackNode) -> RedBlackNode:
        grandparent = parent.parent
        new_subtree_root = parent.left
        if new_subtree_root is None:
            raise RuntimeError("NEW SUBTREE ROOT SHOULD BE TRUE NODE")

        child = new_subtree_root.right

        parent.left = child
        if child is not None:
            child.parent = parent

        new_subtree_root.right = parent
        parent.parent = new_subtree_root
        new_subtree_root.parent = grandparent

        if grandparent is not None:
            if grandparent.right is parent:
                grandparent.right = new_subtree_root
            else:
                grandparent.left = new_subtree_root
        else:
            self.root = new_subtree_root

        return new_subtree_root


def find(root, price: float) -> RedBlackNode:
    if root is None or math.isclose(root.price, price):
        return root

    if root.price < price:
        return find(root=root.right, price=price)

    return find(root=root.left, price=price)


def find_brother(node) -> RedBlackNode:
    if node is None or node.parent is None:
        return None

    parent = node.parent
    return parent.left if node is parent.right else parent.right


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


def print_tree(root: RedBlackNode, level=0):
    if root is not None:
        print_tree(root.left, level + 1)
        print(
            "-" * 4 * level
            + ">"
            + str(root.price)
            + ("R" if root.color == NodeColor.RED else "B")
        )
        print_tree(root.right, level + 1)


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
