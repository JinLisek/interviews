import re

import pytest

from ..process_order import process_order
from ..tree_order_book import TreeOrderBook


def test_asks_should_be_empty_by_default(tree_order_book: TreeOrderBook):
    assert tree_order_book.orders == {}


@pytest.mark.parametrize("side", ["B", "S"])
def test_after_adding_one_order_there_should_be_one_order(
    tree_order_book: TreeOrderBook, side
):
    ticker = "ZZZZ"
    process_order(
        order_book=tree_order_book, order=f"123|z42|a|{ticker}|{side}|7.77777|1"
    )

    assert ticker in tree_order_book.orders


def test_after_adding_one_ask_root_should_have_its_order_id(
    tree_order_book: TreeOrderBook,
):
    order_id = "LOL"
    ticker = "ZZZZ"
    process_order(
        order_book=tree_order_book, order=f"123|{order_id}|a|{ticker}|S|7.77777|1"
    )

    tree_root = tree_order_book.orders[ticker]["asks"].root
    assert tree_root is not None
    assert tree_root.order.order_id == order_id


def test_after_adding_one_ask_root_should_have_its_timestamp(
    tree_order_book: TreeOrderBook,
):
    timestamp = "123"
    ticker = "ZZZZ"
    process_order(
        order_book=tree_order_book, order=f"{timestamp}|z42|a|{ticker}|S|7.77777|1"
    )

    tree_root = tree_order_book.orders[ticker]["asks"].root
    assert tree_root is not None
    assert tree_root.order.timestamp == timestamp


def test_after_adding_one_ask_root_should_have_its_price(
    tree_order_book: TreeOrderBook,
):
    price = 54321.1
    ticker = "ZZZZ"
    process_order(order_book=tree_order_book, order=f"123|z42|a|{ticker}|S|{price}|1")

    tree_root = tree_order_book.orders[ticker]["asks"].root
    assert tree_root is not None
    assert tree_root.order.price == pytest.approx(price)


def test_after_adding_one_ask_root_should_have_its_size(
    tree_order_book: TreeOrderBook,
):
    size = 1337
    ticker = "ZZZZ"
    process_order(
        order_book=tree_order_book, order=f"123|z42|a|{ticker}|S|7.77777|{size}"
    )

    tree_root = tree_order_book.orders[ticker]["asks"].root
    assert tree_root is not None
    assert tree_root.order.size == size


def test_after_two_asks_in_ascending_order_root_should_have_lower_price(
    tree_order_book: TreeOrderBook,
):
    ticker = "ZZZZ"
    lower_price = 1.0
    process_order(
        order_book=tree_order_book, order=f"123|z42|a|{ticker}|S|{lower_price}|1"
    )
    process_order(order_book=tree_order_book, order=f"123|z44|a|{ticker}|S|7.77777|1")

    tree_root = tree_order_book.orders[ticker]["asks"].root
    assert tree_root is not None
    assert tree_root.order.price == pytest.approx(lower_price)


def test_after_two_asks_in_ascending_order_right_child_should_have_higher_price(
    tree_order_book: TreeOrderBook,
):
    ticker = "ZZZZ"
    higher_price = 100.0
    process_order(order_book=tree_order_book, order=f"123|z42|a|{ticker}|S|7.77777|1")
    process_order(
        order_book=tree_order_book, order=f"123|z44|a|{ticker}|S|{higher_price}|1"
    )

    tree_root = tree_order_book.orders[ticker]["asks"].root
    assert tree_root is not None
    assert tree_root.right.order.price == pytest.approx(higher_price)


def test_after_two_asks_in_ascending_order_right_child_should_have_proper_id(
    tree_order_book: TreeOrderBook,
):
    ticker = "ZZZZ"
    second_order_id = "second"
    process_order(order_book=tree_order_book, order=f"123|z42|a|{ticker}|S|7.77777|1")
    process_order(
        order_book=tree_order_book,
        order=f"123|{second_order_id}|a|{ticker}|S|8.88888|1",
    )

    tree_root = tree_order_book.orders[ticker]["asks"].root
    assert tree_root is not None
    assert tree_root.right.order.order_id == second_order_id


def test_after_two_asks_in_descending_order_root_should_have_higher_price(
    tree_order_book: TreeOrderBook,
):
    ticker = "ZZZZ"
    higher_price = 100.0
    process_order(
        order_book=tree_order_book, order=f"123|z42|a|{ticker}|S|{higher_price}|1"
    )
    process_order(order_book=tree_order_book, order=f"123|z44|a|{ticker}|S|7.77777|1")

    tree_root = tree_order_book.orders[ticker]["asks"].root
    assert tree_root is not None
    assert tree_root.order.price == pytest.approx(higher_price)


def test_after_two_asks_in_descending_order_left_child_should_have_lower_price(
    tree_order_book: TreeOrderBook,
):
    ticker = "ZZZZ"
    lower_price = 1.0
    process_order(order_book=tree_order_book, order=f"123|z42|a|{ticker}|S|7.77777|1")
    process_order(
        order_book=tree_order_book, order=f"123|z44|a|{ticker}|S|{lower_price}|1"
    )

    tree_root = tree_order_book.orders[ticker]["asks"].root
    assert tree_root is not None
    assert tree_root.left.order.price == pytest.approx(lower_price)


def test_after_two_asks_in_descending_order_left_child_should_have_proper_id(
    tree_order_book: TreeOrderBook,
):
    ticker = "ZZZZ"
    second_order_id = "second"
    process_order(order_book=tree_order_book, order=f"123|z42|a|{ticker}|S|7.77777|1")
    process_order(
        order_book=tree_order_book,
        order=f"123|{second_order_id}|a|{ticker}|S|6.66666|1",
    )

    tree_root = tree_order_book.orders[ticker]["asks"].root
    assert tree_root is not None
    assert tree_root.left.order.order_id == second_order_id


def test_order_with_size_zero_should_not_be_added_to_book(
    tree_order_book: TreeOrderBook,
):
    process_order(order_book=tree_order_book, order="123|a42|a|ZZZZ|X|7.77777|0")

    assert tree_order_book.orders == {}


def test_order_with_duplicated_id_should_not_be_added_to_book(
    tree_order_book: TreeOrderBook,
):
    ticker_of_duplicated_order = "ZZZZ"
    process_order(order_book=tree_order_book, order="124|z42|a|ZZZY|B|8.88888|2")
    process_order(order_book=tree_order_book, order="123|z42|a|ZZZZ|S|7.77777|1")

    assert ticker_of_duplicated_order not in tree_order_book.orders.keys()


def test_trying_to_add_order_with_duplicated_id_should_log_error(
    tree_order_book: TreeOrderBook, capsys
):
    duplicated_id = "aabb1"

    process_order(
        order_book=tree_order_book, order=f"123|{duplicated_id}|a|ZZZY|B|8.88888|2"
    )
    process_order(
        order_book=tree_order_book, order=f"124|{duplicated_id}|a|ZZZZ|S|7.77777|1"
    )

    error_regex = re.compile(f"ERROR.*{duplicated_id}")
    assert error_regex.match(capsys.readouterr().err)
