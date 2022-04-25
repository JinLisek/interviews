from __future__ import annotations

import math
from enum import Enum, auto, unique
from typing import Optional

from ..order import Order
from ..order_book import OrderBookError


class NodeNotFoundInTree(OrderBookError):
    pass


class OrderNotFoundInNodeOrders(OrderBookError):
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
        node_to_update = find(node=self.root, price=order.price)
        if node_to_update is None:
            raise NodeNotFoundInTree(
                f"Cannot update size of nonexistent order: {order.order_id} with price: {order.price}"
            )

        if order.order_id not in node_to_update.orders:
            raise OrderNotFoundInNodeOrders(
                f"Cannot update size of nonexistent order: {order.order_id} with price {order.price}"
            )

        node_to_update.orders[order.order_id].size = order.size

    def delete(self, order: Order) -> None:
        node_to_remove = find(node=self.root, price=order.price)
        if node_to_remove is None:
            raise NodeNotFoundInTree(
                f"Cannot remove nonexistent order: {order.order_id} with price: {order.price}"
            )

        if len(node_to_remove.orders) > 1:
            del node_to_remove.orders[order.order_id]
            return

        current_node = node_to_remove
        current_node_original_color = current_node.color

        if node_to_remove.left is None:
            child = node_to_remove.right
            self.__transplant(parent=node_to_remove, child=node_to_remove.right)
        elif node_to_remove.right is None:
            child = node_to_remove.left
            self.__transplant(parent=node_to_remove, child=node_to_remove.left)
        else:
            current_node = minimal_node(root=node_to_remove.right)
            current_node_original_color = current_node.color
            child = current_node.right
            if current_node.parent is node_to_remove:
                if child is not None:
                    child.parent = current_node
            else:
                self.__transplant(parent=current_node, child=current_node.right)
                current_node.right = node_to_remove.right
                current_node.right.parent = current_node

            self.__transplant(parent=node_to_remove, child=current_node)
            current_node.left = node_to_remove.left
            current_node.left.parent = current_node
            current_node.color = node_to_remove.color

        if current_node_original_color == NodeColor.BLACK:
            self.fix_delete(node=child)

    def fix_delete(self, node: RedBlackNode) -> None:
        while (
            node is not None and node is not self.root and node.color == NodeColor.BLACK
        ):
            if node is node.parent.left:
                sibling = node.parent.right
                if sibling is not None and sibling.color == NodeColor.RED:
                    sibling.color = NodeColor.BLACK
                    node.parent.color = NodeColor.RED
                    self.__rotate_left(parent=node.parent)
                    sibling = node.parent.right
                if (
                    sibling is not None
                    and (sibling.left is None or sibling.left.color == NodeColor.BLACK)
                    and (
                        sibling.right is None or sibling.right.color == NodeColor.BLACK
                    )
                ):
                    sibling.color = NodeColor.RED
                    node = node.parent
                else:
                    if (
                        sibling is not None
                        and sibling.right is not None
                        and sibling.right.color == NodeColor.BLACK
                    ):
                        sibling.left.color = NodeColor.BLACK
                        sibling.color = NodeColor.RED
                        self.__rotate_right(parent=sibling)
                        sibling = node.parent.right

                    if sibling is not None:
                        sibling.color = node.parent.color
                        if sibling.right is not None:
                            sibling.right.color = NodeColor.BLACK
                    node.parent.color = NodeColor.BLACK
                    self.__rotate_left(parent=node.parent)
                    node = self.root
            else:
                sibling = node.parent.left
                if sibling is not None and sibling.color == NodeColor.RED:
                    sibling.color = NodeColor.BLACK
                    node.parent.color = NodeColor.RED
                    self.__rotate_right(parent=node.parent)
                    sibling = node.parent.left

                if (
                    sibling is not None
                    and (sibling.left is None or sibling.left.color == NodeColor.BLACK)
                    and (
                        sibling.right is None or sibling.right.color == NodeColor.BLACK
                    )
                ):
                    sibling.color = NodeColor.RED
                    node = node.parent
                else:
                    if (
                        sibling is not None
                        and sibling.left is not None
                        and sibling.left.color == NodeColor.BLACK
                    ):
                        sibling.right.color = NodeColor.BLACK
                        sibling.color = NodeColor.RED
                        self.__rotate_left(parent=sibling)
                        sibling = node.parent.left

                    if sibling is not None:
                        sibling.color = node.parent.color
                        if sibling.left is not None:
                            sibling.left.color = NodeColor.BLACK
                    node.parent.color = NodeColor.BLACK
                    self.__rotate_right(parent=node.parent)
                    node = self.root
        if node is not None:
            node.color = NodeColor.BLACK

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

    def __rotate_left(self, parent: RedBlackNode) -> None:
        grandparent = parent.parent
        new_subtree_root = parent.right
        if new_subtree_root is None:
            return

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

    def __rotate_right(self, parent: RedBlackNode) -> None:
        grandparent = parent.parent
        new_subtree_root = parent.left
        if new_subtree_root is None:
            return

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

    def swap_nodes(self, first: RedBlackNode, second: RedBlackNode, /) -> None:
        print("SWAP NODES")
        if first is second.parent:
            print("SWAP NODES -- first is parent of second")
            swap_parent_and_child(parent=first, child=second)
        elif second is first.parent:
            print("SWAP NODES -- second is parent of first")
            swap_parent_and_child(parent=second, child=first)
        else:
            if first.parent is not None:
                if first is first.parent.left:
                    first.parent.left = second
                else:
                    first.parent.right = second

            if second.parent is not None:
                if second is second.parent.left:
                    second.parent.left = first
                else:
                    second.parent.right = first

            first.parent, second.parent = second.parent, first.parent
            first.color, second.color = second.color, first.color
            first.left, second.left = second.left, first.left
            first.right, second.right = second.right, first.right

            if first.left is not None:
                first.left.parent = first
            if first.right is not None:
                first.right.parent = first

            if second.left is not None:
                second.left.parent = second
            if second.right is not None:
                second.right.parent = second

        if self.root is first:
            self.root = second
        elif self.root is second:
            self.root = first

    def print_tree(self) -> None:
        print_tree(root=self.root)


def find(node: RedBlackNode, price: float) -> RedBlackNode:
    if node is None or math.isclose(node.price, price):
        return node

    if node.price < price:
        return find(node=node.right, price=price)

    return find(node=node.left, price=price)


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


def swap_parent_and_child(*, parent: RedBlackNode, child: RedBlackNode) -> None:
    if child is parent.right:
        print("child is right of parent")
        child_right = child.right
        print(f"child has right: {child_right}")
        child.right = parent
        print(f"child should have parent as right: {child.right}")
        parent.right = child_right
        print(f"parent should have None as right: {parent.right}")

        if parent.right is not None:
            parent.right.parent = parent
        parent.left, child.left = child.left, parent.left
    elif child is parent.left:
        print("child is left of parent")
        child_left = child.left
        child.left = parent
        parent.left = child_left

        if parent.left is not None:
            parent.left.parent = parent
        parent.right, child.right = child.right, parent.right
    else:
        raise RuntimeError("NOT PARENT AND CHILD RELATION")

    print(f"parent should have None as right: {parent.right}")

    grandparent = parent.parent
    parent.parent = child
    child.parent = grandparent
    parent.color, child.color = child.color, parent.color

    print(f"parent {parent.price} has left: {parent.left} and right: {parent.right}")
    print(f"child {child.price} has left: {child.left} and right: {child.right}")


def remove_node_from_parent(node: RedBlackNode, /) -> None:
    if node.parent is None:
        return

    if node is node.parent.left:
        node.parent.left = None
    elif node is node.parent.right:
        node.parent.right = None
