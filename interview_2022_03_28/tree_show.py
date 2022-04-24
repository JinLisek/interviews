from .order_processing.order import Order, OrderType
from .order_processing.tree_order_book import RedBlackTree, print_tree


class OrderIds:
    def __init__(self):
        self.__current = 1

    def __iter__(self):
        return self

    def __next__(self):
        result = self.__current
        self.__current += 1
        return str(result)


ORDER_IDS = OrderIds()
ORDER_ID_GENERATOR = iter(ORDER_IDS)

added_orders = []


def create_add_order(price: float) -> Order:
    return Order(
        order_id=next(ORDER_ID_GENERATOR),
        timestamp="123",
        ticker="blabla",
        price=price,
        size=10,
        order_type=OrderType.BID,
    )


def main():
    tree = RedBlackTree()

    for price in range(1, 50):
        order = create_add_order(price=price)
        tree.insert(order=order)
        added_orders.append(order)
    print_tree(tree.root)
    print("=" * 100)

    print("Y" * 100)

    for cancelled_order in added_orders:
        tree.remove(order=cancelled_order)
        print_tree(tree.root)
        print("=" * 100)


if __name__ == "__main__":
    main()
