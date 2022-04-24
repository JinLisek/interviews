from ..order import Order


class Node:
    def __init__(self, order: Order):
        self.parent = None
        self.left = None
        self.right = None
        self.color = 1

        self.price = order.price

        self.orders = {}
        self.orders[order.order_id] = order


class RedBlackTree:
    def __init__(self):
        self.root = None

    # Preorder
    def pre_order_helper(self, node):
        if node is not None:
            print(node.price + " ")
            self.pre_order_helper(node.left)
            self.pre_order_helper(node.right)

    # Inorder
    def in_order_helper(self, node):
        if node is not None:
            self.in_order_helper(node.left)
            print(node.price + " ")
            self.in_order_helper(node.right)

    # Postorder
    def post_order_helper(self, node):
        if node is not None:
            self.post_order_helper(node.left)
            self.post_order_helper(node.right)
            print(node.price + " ")

    # Search the tree
    def search_tree_helper(self, node, price):
        if node is None or price == node.price:
            return node

        if price < node.price:
            return self.search_tree_helper(node.left, price)
        return self.search_tree_helper(node.right, price)

    # Balancing the tree after deletion
    def delete_fix(self, x):
        while x != self.root and x is not None and x.color == 0:
            if x == x.parent.left:
                s = x.parent.right
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.left_rotate(x.parent)
                    s = x.parent.right

                if s.left.color == 0 and s.right.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.right.color == 0:
                        s.left.color = 0
                        s.color = 1
                        self.right_rotate(s)
                        s = x.parent.right

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.right.color = 0
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                s = x.parent.left
                if s.color == 1:
                    s.color = 0
                    x.parent.color = 1
                    self.right_rotate(x.parent)
                    s = x.parent.left

                if s.right.color == 0 and s.left.color == 0:
                    s.color = 1
                    x = x.parent
                else:
                    if s.left.color == 0:
                        s.right.color = 0
                        s.color = 1
                        self.left_rotate(s)
                        s = x.parent.left

                    s.color = x.parent.color
                    x.parent.color = 0
                    s.left.color = 0
                    self.right_rotate(x.parent)
                    x = self.root
        if x is not None:
            x.color = 0

    def __rb_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        elif u == u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v

        if v is not None:
            v.parent = u.parent

    # Node deletion
    def delete_node_helper(self, node, order: Order):
        z = None
        while node is not None:
            if node.price == order.price:
                z = node

            if node.price <= order.price:
                node = node.right
            else:
                node = node.left

        if z is None:
            print("Cannot find price in the tree")
            return

        if len(z.orders) > 1:
            del z.orders[order.order_id]
            return

        y = z
        y_original_color = y.color
        if z.left is None:
            x = z.right
            self.__rb_transplant(z, z.right)
        elif z.right is None:
            x = z.left
            self.__rb_transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_original_color = y.color
            x = y.right
            if y.parent == z:
                if x is not None:
                    x.parent = y
            else:
                self.__rb_transplant(y, y.right)
                y.right = z.right
                y.right.parent = y

            self.__rb_transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        if y_original_color == 0:
            self.delete_fix(x)

    # Balance the tree after insertion
    def fix_insert(self, k):
        while k.parent.color == 1:
            if k.parent == k.parent.parent.right:
                u = k.parent.parent.left
                if u is not None and u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.left:
                        k = k.parent
                        self.right_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.left_rotate(k.parent.parent)
            else:
                u = k.parent.parent.right

                if u is not None and u.color == 1:
                    u.color = 0
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    k = k.parent.parent
                else:
                    if k == k.parent.right:
                        k = k.parent
                        self.left_rotate(k)
                    k.parent.color = 0
                    k.parent.parent.color = 1
                    self.right_rotate(k.parent.parent)
            if k == self.root:
                break
        self.root.color = 0

    def __print_helper(self, node: Node, level=0):
        if node is None:
            return
        self.__print_helper(node.left, level + 1)
        print(
            "-" * 4 * level + ">" + str(node.price) + ("R" if node.color == 1 else "B")
        )
        self.__print_helper(node.right, level + 1)

    def preorder(self):
        self.pre_order_helper(self.root)

    def inorder(self):
        self.in_order_helper(self.root)

    def postorder(self):
        self.post_order_helper(self.root)

    def searchTree(self, k):
        return self.search_tree_helper(self.root, k)

    def minimum(self, node):
        while node.left is not None:
            node = node.left
        return node

    def maximum(self, node):
        while node.right is not None:
            node = node.right
        return node

    def get_minimum(self) -> float:
        if self.root is None:
            return 0.0

        min_node = self.minimum(node=self.root)

        if min_node is None:
            return 0.0

        return min_node.price

    def get_maximum(self) -> float:
        if self.root is None:
            return 0.0

        max_node = self.maximum(node=self.root)

        if max_node is None:
            return 0.0

        return max_node.price

    def successor(self, x):
        if x.right is not None:
            return self.minimum(x.right)

        y = x.parent
        while y is not None and x == y.right:
            x = y
            y = y.parent
        return y

    def predecessor(self, x):
        if x.left is not None:
            return self.maximum(x.left)

        y = x.parent
        while y is not None and x == y.left:
            x = y
            y = y.parent

        return y

    def left_rotate(self, x):
        y = x.right
        x.right = y.left
        if y.left is not None:
            y.left.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, x):
        y = x.left
        x.left = y.right
        if y.right is not None:
            y.right.parent = x

        y.parent = x.parent
        if x.parent == None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def insert(self, order: Order):
        node = Node(order=order)

        y = None
        x = self.root

        while x is not None:
            y = x
            if node.price < x.price:
                x = x.left
            elif node.price > x.price:
                x = x.right
            else:
                x.orders[order.order_id] = order
                return

        node.parent = y
        if y == None:
            self.root = node
        elif node.price < y.price:
            y.left = node
        else:
            y.right = node

        if node.parent == None:
            node.color = 0
            return

        if node.parent.parent == None:
            return

        self.fix_insert(node)

    def get_root(self):
        return self.root

    def delete(self, order: Order):
        self.delete_node_helper(self.root, order=order)

    def update(self, order: Order) -> None:
        node_to_remove = self.search_tree_helper(node=self.root, price=order.price)
        if node_to_remove is None:
            raise RuntimeError(f"BLAX NODE NOT FOUND TO UPDATE price {order.price}")

        node_to_remove.orders[order.order_id].size = order.size

    def print_tree(self):
        self.__print_helper(node=self.root)
