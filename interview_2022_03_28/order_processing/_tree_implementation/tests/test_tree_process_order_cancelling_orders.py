import re

import pytest

from ...order import Order, OrderType
from ...process_order import process_order
from ..tree_order_book import TreeOrderBook


def test_given_empty_tree_then_cancelling_order_should_not_add_orders(
    tree_order_book: TreeOrderBook,
):
    process_order(order_book=tree_order_book, order="789|e11|c")

    assert tree_order_book.orders == {}


@pytest.mark.parametrize(
    "side, container_name, order_type",
    [("B", "bids", OrderType.BID), ("S", "asks", OrderType.ASK)],
)
def test_cancelling_non_existing_order_should_not_modify_existing_orders(
    tree_order_book: TreeOrderBook,
    side: str,
    container_name: str,
    order_type: OrderType,
):
    timestamp = "789"
    order_id = "bbaa"
    ticker = "XXYY"
    price = 4.56789
    size = 8

    process_order(
        order_book=tree_order_book,
        order=f"{timestamp}|{order_id}|a|{ticker}|{side}|{price}|{size}",
    )
    process_order(order_book=tree_order_book, order="789|e11|c")

    tree_root = tree_order_book.orders[ticker][container_name].root
    assert tree_root is not None
    assert tree_root.orders == {
        order_id: Order(
            order_id=order_id,
            timestamp=timestamp,
            ticker=ticker,
            price=price,
            size=size,
            order_type=order_type,
        )
    }


def test_cancelling_non_existing_order_should_log_error(
    tree_order_book: TreeOrderBook, capsys
):
    order_id = "123lol"
    process_order(order_book=tree_order_book, order=f"789|{order_id}|c")

    error_regex = re.compile(f"ERROR.*{order_id}")
    assert error_regex.match(capsys.readouterr().err)


@pytest.mark.parametrize("side, container", [("B", "bids"), ("S", "asks")])
def test_cancelling_existing_order_should_remove_it_from_tree(
    tree_order_book: TreeOrderBook, side: str, container: str
):
    order_id = "bbaa"
    ticker = "SCRUB"

    process_order(
        order_book=tree_order_book, order=f"789|{order_id}|a|{ticker}|{side}|1.2|1"
    )
    process_order(order_book=tree_order_book, order=f"789|{order_id}|c")

    assert tree_order_book.orders[ticker][container].root is None


@pytest.mark.parametrize(
    "side, container, order_type",
    [("B", "bids", OrderType.BID), ("S", "asks", OrderType.ASK)],
)
def test_cancelling_existing_order_should_not_modify_other_orders(
    tree_order_book: TreeOrderBook, side: str, container: str, order_type: OrderType
):
    order_id_to_cancel = "cancelled"

    timestamp = "789"
    id_of_unchanged_order = "bbaa"
    ticker = "XXYY"
    price = 4.56789
    size = 8

    process_order(
        order_book=tree_order_book,
        order=f"{timestamp}|{id_of_unchanged_order}|a|{ticker}|{side}|{price}|{size}",
    )
    process_order(
        order_book=tree_order_book,
        order=f"789|{order_id_to_cancel}|a|{ticker}|{side}|1.2|1",
    )
    process_order(order_book=tree_order_book, order=f"789|{order_id_to_cancel}|c")

    tree_root = tree_order_book.orders[ticker][container].root
    assert tree_root is not None
    assert tree_root.orders == {
        id_of_unchanged_order: Order(
            order_id=id_of_unchanged_order,
            timestamp=timestamp,
            ticker=ticker,
            price=price,
            size=size,
            order_type=order_type,
        )
    }


@pytest.mark.parametrize(
    "side, container, order_type",
    [("B", "bids", OrderType.BID), ("S", "asks", OrderType.ASK)],
)
def test_given_two_orders_with_same_price_cancel_should_remove_proper_order(
    tree_order_book: TreeOrderBook, side: str, container: str, order_type: OrderType
):
    order_id_to_cancel = "cancelled"

    timestamp = "789"
    id_of_unchanged_order = "bbaa"
    ticker = "XXYY"
    price = 4.56789
    size = 8

    process_order(
        order_book=tree_order_book,
        order=f"{timestamp}|{id_of_unchanged_order}|a|{ticker}|{side}|{price}|{size}",
    )
    process_order(
        order_book=tree_order_book,
        order=f"789|{order_id_to_cancel}|a|{ticker}|{side}|{price}|1",
    )
    process_order(order_book=tree_order_book, order=f"789|{order_id_to_cancel}|c")

    tree_root = tree_order_book.orders[ticker][container].root
    assert tree_root is not None
    assert tree_root.orders == {
        id_of_unchanged_order: Order(
            order_id=id_of_unchanged_order,
            timestamp=timestamp,
            ticker=ticker,
            price=price,
            size=size,
            order_type=order_type,
        )
    }
