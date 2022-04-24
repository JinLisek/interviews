import pytest

from ...order import Order, OrderType
from ...process_order import process_order
from ..tree_order_book import TreeOrderBook

CORRECT_ORDER_ID = "bid1"

INCORRECT_INPUTS = [
    "",
    "kugeakufgauk",
    "123|id1",
    "123|id1|",
    "123|z42|INCORRECT-ACTION|ZZZZ|B|7.77777|1",
    "123|z42|a|ZZZZ|INCORRECT-SIDE|3.3|71",
    "123|z42|a|ZZZZ|B|3.3|",
    "123|z42|a|ZZZZ|S|3.3|",
    "123|z42|a|ZZZZ|B|3.3|a",
    "123|z42|a|ZZZZ|S|3.3|a",
    "123|z42|a|ZZZZ|B|3.3|1a",
    "123|z42|a|ZZZZ|S|3.3|1a",
    "123|z42|a|ZZZZ|B|3.3|a1",
    "123|z42|a|ZZZZ|S|3.3|a1",
    "123|z42|a|ZZZZ|B|3.3|0",
    "123|z42|a|ZZZZ|S|3.3|0",
    "123|z42|a|ZZZZ|B|3.3|-1",
    "123|z42|a|ZZZZ|S|3.3|-1",
    "aaa|z42|a|ZZZZ|S|3.3|1",
    "1aa|z42|a|ZZZZ|S|3.3|1",
    "aa1|z42|a|ZZZZ|S|3.3|1",
    "1a1|z42|a|ZZZZ|S|3.3|1",
    "123|#1|a|ZZZZ|S|3.3|1",
    "123|#id|a|ZZZZ|S|3.3|1",
    "123|1#|a|ZZZZ|S|3.3|1",
    "123|id#|a|ZZZZ|S|3.3|1",
    "123|1#2|a|ZZZZ|S|3.3|1",
    "123|i#d|a|ZZZZ|S|3.3|1",
    "123|#1|c",
    "123|#id|c",
    "123|1#|c",
    "123|id#|c",
    "123|1#2|c",
    "123|i#d|c",
    "123|#1|u|1",
    "123|#id|u|1",
    "123|1#|u|1",
    "123|id#|u|1",
    "123|1#2|u|1",
    "123|i#d|u|1",
]


@pytest.mark.parametrize("incorrect_order", INCORRECT_INPUTS)
def test_given_incorrect_order_should_log_error(
    tree_order_book: TreeOrderBook, capsys, incorrect_order: str
):
    process_order(order_book=tree_order_book, order=incorrect_order)

    assert "ERROR" in capsys.readouterr().err


@pytest.mark.parametrize("incorrect_order", INCORRECT_INPUTS)
def test_given_incorrect_order_should_not_add_orders(
    tree_order_book: TreeOrderBook, incorrect_order: str
):
    process_order(order_book=tree_order_book, order=incorrect_order)

    assert tree_order_book.orders == {}


@pytest.mark.parametrize("incorrect_order", INCORRECT_INPUTS)
def test_given_incorrect_order_should_not_modify_existing_orders(
    tree_order_book: TreeOrderBook, incorrect_order: str
):
    timestamp = "123"
    order_id = "correctid"
    ticker = "KCIT"
    price = 8.54321
    size = 17

    process_order(
        order_book=tree_order_book,
        order=f"{timestamp}|{order_id}|a|{ticker}|B|{price}|{size}",
    )
    process_order(order_book=tree_order_book, order=incorrect_order)

    tree_root = tree_order_book.orders[ticker]["bids"].root
    assert tree_root is not None
    assert tree_root.left is None
    assert tree_root.right is None
    assert tree_root.orders == {
        order_id: Order(
            order_id=order_id,
            timestamp=timestamp,
            ticker=ticker,
            price=price,
            size=size,
            order_type=OrderType.BID,
        )
    }


@pytest.fixture(name="add_correct_order")
def fixture_add_correct_order(tree_order_book: TreeOrderBook) -> None:
    process_order(
        order_book=tree_order_book, order=f"123|{CORRECT_ORDER_ID}|a|ZZZZ|B|3.3|1"
    )


@pytest.mark.parametrize(
    "incorrect_order",
    [
        f"aa|{CORRECT_ORDER_ID}|c",
        f"1a|{CORRECT_ORDER_ID}|c",
        f"a1|{CORRECT_ORDER_ID}|c",
        f"1a1|{CORRECT_ORDER_ID}|c",
        f"123|{CORRECT_ORDER_ID}|u",
        f"123|{CORRECT_ORDER_ID}|u|",
        f"123|{CORRECT_ORDER_ID}|u|a",
        f"123|{CORRECT_ORDER_ID}|u|1a",
        f"123|{CORRECT_ORDER_ID}|u|a1",
        f"123|{CORRECT_ORDER_ID}|u|0",
        f"123|{CORRECT_ORDER_ID}|u|-1",
        f"123|{CORRECT_ORDER_ID}|u|-1",
        f"aa|{CORRECT_ORDER_ID}|u|1",
        f"1a|{CORRECT_ORDER_ID}|u|1",
        f"a1|{CORRECT_ORDER_ID}|u|1",
        f"1a1|{CORRECT_ORDER_ID}|u|1",
    ],
)
@pytest.mark.usefixtures("add_correct_order")
class TestInvalidInputWithCorrectOrderInDatabase:
    @staticmethod
    def test_given_incorrect_order_should_log_error(
        tree_order_book: TreeOrderBook, capsys, incorrect_order: str
    ):
        process_order(order_book=tree_order_book, order=incorrect_order)

        assert "ERROR" in capsys.readouterr().err

    @staticmethod
    def test_given_incorrect_order_should_not_modify_existing_orders(
        tree_order_book: TreeOrderBook, incorrect_order: str
    ):
        timestamp = "123"
        order_id = "correctid"
        ticker = "KCIT"
        price = 8.54321
        size = 17

        process_order(
            order_book=tree_order_book,
            order=f"{timestamp}|{order_id}|a|{ticker}|B|{price}|{size}",
        )
        process_order(order_book=tree_order_book, order=incorrect_order)

        tree_root = tree_order_book.orders[ticker]["bids"].root
        assert tree_root is not None
        assert tree_root.left is None
        assert tree_root.right is None
        assert tree_root.orders == {
            order_id: Order(
                order_id=order_id,
                timestamp=timestamp,
                ticker=ticker,
                price=price,
                size=size,
                order_type=OrderType.BID,
            )
        }
