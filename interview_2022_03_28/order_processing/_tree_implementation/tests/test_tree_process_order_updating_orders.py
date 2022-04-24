import re

import pytest

from ...order import Order, OrderType
from ...process_order import process_order
from ..tree_order_book import TreeOrderBook


def test_given_empty_tree_updating_order_should_not_add_orders(
    tree_order_book: TreeOrderBook,
):
    process_order(order_book=tree_order_book, order="456|1o1|u|20")

    assert tree_order_book.orders == {}


def test_given_empty_tree_updating_order_should_log_error(
    tree_order_book: TreeOrderBook, capsys
):
    order_id = "1o1"
    process_order(order_book=tree_order_book, order=f"456|{order_id}|u|20")

    error_regex = re.compile(f"ERROR.*{order_id}")
    assert error_regex.match(capsys.readouterr().err)


@pytest.mark.parametrize(
    "side, container, order_type",
    [("B", "bids", OrderType.BID), ("S", "asks", OrderType.ASK)],
)
def test_updating_non_existing_order_should_not_modify_other_orders(
    tree_order_book: TreeOrderBook, side: str, container: str, order_type: OrderType
):
    id_of_updated_order = "upd11"

    timestamp = "789"
    id_of_unchanged_order = "bbaa"
    ticker = "XXYY"
    price = 4.56789
    size = 8

    process_order(
        order_book=tree_order_book,
        order=f"{timestamp}|{id_of_unchanged_order}|a|{ticker}|{side}|{price}|{size}",
    )

    process_order(order_book=tree_order_book, order=f"789|{id_of_updated_order}|u|1001")

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
def test_updating_existing_order_should_not_modify_other_orders(
    tree_order_book: TreeOrderBook, side: str, container: str, order_type: OrderType
):
    id_of_updated_order = "updated"

    timestamp = "789"
    id_of_unchanging_order = "bbaa"
    ticker = "XXYY"
    price = 4.56789
    size = 8

    process_order(
        order_book=tree_order_book,
        order=f"{timestamp}|{id_of_unchanging_order}|a|{ticker}|{side}|{price}|{size}",
    )

    process_order(
        order_book=tree_order_book,
        order=f"456|{id_of_updated_order}|a|{ticker}|{side}|1.2|3",
    )

    process_order(order_book=tree_order_book, order=f"456|{id_of_updated_order}|u|20")

    tree_root = tree_order_book.orders[ticker][container].root
    assert tree_root is not None
    assert tree_root.orders == {
        id_of_unchanging_order: Order(
            order_id=id_of_unchanging_order,
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
def test_updating_existing_order_should_change_its_size(
    tree_order_book: TreeOrderBook, side: str, container: str, order_type: OrderType
):
    ticker = "SCRUB"
    new_size = 88

    order_id = "bbaa"
    price = 1.2
    timestamp = "789"

    process_order(
        order_book=tree_order_book,
        order=f"{timestamp}|{order_id}|a|{ticker}|{side}|{price}|1",
    )
    process_order(order_book=tree_order_book, order=f"10|{order_id}|u|{new_size}")

    tree_root = tree_order_book.orders[ticker][container].root
    assert tree_root is not None
    assert tree_root.orders == {
        order_id: Order(
            order_id=order_id,
            timestamp=timestamp,
            ticker=ticker,
            price=price,
            size=new_size,
            order_type=order_type,
        )
    }


@pytest.mark.parametrize(
    "side, container, order_type",
    [("B", "bids", OrderType.BID), ("S", "asks", OrderType.ASK)],
)
def test_given_two_orders_with_same_price_updating_one_of_them_should_change_only_its_size(
    tree_order_book: TreeOrderBook, side: str, container: str, order_type: OrderType
):
    ticker = "TICK"
    price = 1.2

    first_order_id = "bbaa"
    first_timestamp = "789"
    first_size = 100

    second_order_id = "bbcc"
    second_timestamp = "456"
    second_old_size = 200
    second_new_size = 2000

    process_order(
        order_book=tree_order_book,
        order=f"{first_timestamp}|{first_order_id}|a|{ticker}|{side}|{price}|{first_size}",
    )
    process_order(
        order_book=tree_order_book,
        order=f"{second_timestamp}|{second_order_id}|a|{ticker}|{side}|{price}|{second_old_size}",
    )
    process_order(
        order_book=tree_order_book, order=f"10|{second_order_id}|u|{second_new_size}"
    )

    tree_root = tree_order_book.orders[ticker][container].root
    assert tree_root is not None
    assert tree_root.orders == {
        first_order_id: Order(
            order_id=first_order_id,
            timestamp=first_timestamp,
            ticker=ticker,
            price=price,
            size=first_size,
            order_type=order_type,
        ),
        second_order_id: Order(
            order_id=second_order_id,
            timestamp=second_timestamp,
            ticker=ticker,
            price=price,
            size=second_new_size,
            order_type=order_type,
        ),
    }
