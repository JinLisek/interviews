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
        # current_node = find(node=self.root, price=order.price)
        # if current_node is None:
        #     raise RuntimeError(f"BLAX NODE NOT FOUND TO REMOVE price {order.price}")

        # if len(current_node.orders) > 1:
        #     del current_node.orders[order.order_id]
        #     return

        # if (
        #     current_node is self.root
        #     and self.root.left is None
        #     and self.root.right is None
        # ):
        #     # simple case: current_node is childless root
        #     print(f"REMOVING {order.price} is childless root")
        #     self.root = None
        #     return

        # if current_node.left is not None and current_node.right is not None:
        #     print(f"REMOVING {order.price} has 2 children")
        #     # simple case: current_node has 2 children
        #     successor = minimal_node(current_node.right)
        #     self.swap_nodes(current_node, successor)
        #     if current_node is self.root:
        #         self.root = successor

        # if current_node.color == NodeColor.RED:
        #     # simple case: current_node is red
        #     # so at this point it cannot have any children and can just be removed
        #     print(f"REMOVING {order.price} is RED, removing")
        #     remove_node_from_parent(current_node)
        #     return

        # # simple case: current_node is black
        # # it might have 1 red child or no children
        # if current_node.left is not None:
        #     print(f"REMOVING {order.price} BLACK and has left child, swapping")
        #     self.swap_nodes(current_node, current_node.left)
        #     if current_node is self.root:
        #         self.root = current_node.left
        # elif current_node.right is not None:
        #     print(f"REMOVING {order.price} BLACK and has right child, swapping")
        #     right = current_node.right
        #     self.swap_nodes(current_node, current_node.right)
        #     if current_node is self.root:
        #         self.root = current_node.right
        #     print(
        #         f"current_node.right after swapping {right.price}, parent {right.parent}"
        #     )
        # print(
        #     f"current_node after swapping {current_node.price}, parent {current_node.parent}"
        # )

        # # loop?
        # # complex case: current_node is not root, is black and has no children
        # parent = current_node.parent
        # sibling = None

        # direction_from_parent = "left" if parent.left is current_node else "right"
        # if current_node is parent.left:
        #     sibling = parent.right
        # elif current_node is parent.right:
        #     sibling = parent.left

        # remove_node_from_parent(current_node)

        # if sibling.color == NodeColor.RED:
        #     # deletion case 3: sibling is red, so parent is black, and both nephews are black
        #     if direction_from_parent == "left":
        #         self.__rotate_left(parent=parent)
        #     elif direction_from_parent == "right":
        #         self.__rotate_right(parent=parent)
        #     else:
        #         raise RuntimeError("UNKNOWN DIRECTIOn")
        #     parent.color = NodeColor.RED
        #     sibling.color = NodeColor.BLACK

        node_to_remove = find(node=self.root, price=order.price)
        if node_to_remove is None:
            raise NodeNotFoundInTree(
                f"Cannot remove nonexistent order: {order.order_id} with price: {order.price}"
            )

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
                if right_child_of_minimal_right is not None:
                    right_child_of_minimal_right.parent = minimal_right
            else:
                self.__transplant(parent=minimal_right, child=minimal_right.right)
                minimal_right.right = node_to_remove.right
                minimal_right.right.parent = minimal_right

            self.__transplant(parent=node_to_remove, child=minimal_right)
            minimal_right.left = node_to_remove.left
            minimal_right.left.parent = minimal_right
            minimal_right.color = node_to_remove.color

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
