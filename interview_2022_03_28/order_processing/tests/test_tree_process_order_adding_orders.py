import re

import pytest

from ..order import Order, OrderType
from ..process_order import process_order
from ..tree_order_book import TreeOrderBook


def test_orders_should_be_empty_by_default(tree_order_book: TreeOrderBook):
    assert tree_order_book.orders == {}


@pytest.mark.parametrize(
    "side, container_name, order_type",
    [("B", "bids", OrderType.BID), ("S", "asks", OrderType.ASK)],
)
def test_after_adding_one_order_root_should_contain_its_data(
    tree_order_book: TreeOrderBook,
    side: str,
    container_name: str,
    order_type: OrderType,
):
    order_id = "LOL"
    timestamp = "123"
    ticker = "ZZZZ"
    price = 54321.1
    size = 1337

    process_order(
        order_book=tree_order_book,
        order=f"{timestamp}|{order_id}|a|{ticker}|{side}|{price}|{size}",
    )

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


@pytest.mark.parametrize(
    "side, container, order_type",
    [("B", "bids", OrderType.BID), ("S", "asks", OrderType.ASK)],
)
def test_after_adding_two_orders_in_ascending_order_root_should_have_lower_price(
    tree_order_book: TreeOrderBook, side: str, container: str, order_type: OrderType
):
    ticker = "ZZZZ"

    order_id = "FIRST"
    timestamp = "123"
    lower_price = 1.0
    size = 88

    process_order(
        order_book=tree_order_book,
        order=f"{timestamp}|{order_id}|a|{ticker}|{side}|{lower_price}|{size}",
    )
    process_order(
        order_book=tree_order_book, order=f"456|SECOND|a|{ticker}|{side}|7.77777|1"
    )

    tree_root = tree_order_book.orders[ticker][container].root
    assert tree_root is not None
    assert tree_root.orders == {
        order_id: Order(
            order_id=order_id,
            timestamp=timestamp,
            ticker=ticker,
            price=lower_price,
            size=size,
            order_type=order_type,
        )
    }


@pytest.mark.parametrize(
    "side, container, order_type",
    [("B", "bids", OrderType.BID), ("S", "asks", OrderType.ASK)],
)
def test_after_adding_two_orders_in_ascending_order_right_child_should_have_higher_price(
    tree_order_book: TreeOrderBook, side: str, container: str, order_type: OrderType
):
    ticker = "ZZZZ"

    order_id = "SECOND"
    timestamp = "456"
    higher_price = 100.0
    size = 88

    process_order(
        order_book=tree_order_book, order=f"123|FIRST|a|{ticker}|{side}|7.77777|1"
    )
    process_order(
        order_book=tree_order_book,
        order=f"{timestamp}|{order_id}|a|{ticker}|{side}|{higher_price}|{size}",
    )

    tree_root = tree_order_book.orders[ticker][container].root
    assert tree_root is not None
    assert tree_root.right.orders == {
        order_id: Order(
            order_id=order_id,
            timestamp=timestamp,
            ticker=ticker,
            price=higher_price,
            size=size,
            order_type=order_type,
        )
    }


@pytest.mark.parametrize(
    "side, container, order_type",
    [("B", "bids", OrderType.BID), ("S", "asks", OrderType.ASK)],
)
def test_after_two_orders_in_descending_order_root_should_have_higher_price(
    tree_order_book: TreeOrderBook, side: str, container: str, order_type: OrderType
):
    ticker = "ZZZZ"

    order_id = "FIRST"
    timestamp = "123"
    higher_price = 100.0
    size = 88

    process_order(
        order_book=tree_order_book,
        order=f"{timestamp}|{order_id}|a|{ticker}|{side}|{higher_price}|{size}",
    )
    process_order(
        order_book=tree_order_book, order=f"456|SECOND|a|{ticker}|{side}|7.77777|1"
    )

    tree_root = tree_order_book.orders[ticker][container].root
    assert tree_root is not None
    assert tree_root.orders == {
        order_id: Order(
            order_id=order_id,
            timestamp=timestamp,
            ticker=ticker,
            price=higher_price,
            size=size,
            order_type=order_type,
        )
    }


@pytest.mark.parametrize(
    "side, container, order_type",
    [("B", "bids", OrderType.BID), ("S", "asks", OrderType.ASK)],
)
def test_after_two_orders_in_descending_order_left_child_should_have_lower_price(
    tree_order_book: TreeOrderBook, side: str, container: str, order_type: OrderType
):
    ticker = "ZZZZ"

    order_id = "SECOND"
    timestamp = "123"
    lower_price = 1.0
    size = 88

    process_order(
        order_book=tree_order_book, order=f"123|FIRST|a|{ticker}|{side}|7.77777|1"
    )
    process_order(
        order_book=tree_order_book,
        order=f"{timestamp}|{order_id}|a|{ticker}|{side}|{lower_price}|{size}",
    )

    tree_root = tree_order_book.orders[ticker][container].root
    assert tree_root is not None
    assert tree_root.left.orders == {
        order_id: Order(
            order_id=order_id,
            timestamp=timestamp,
            ticker=ticker,
            price=lower_price,
            size=size,
            order_type=order_type,
        )
    }


@pytest.mark.parametrize("side", ["B", "S"])
def test_order_with_size_zero_should_not_be_added_to_book(
    tree_order_book: TreeOrderBook, side: str
):
    process_order(order_book=tree_order_book, order=f"123|a42|a|ZZZZ|{side}|7.77777|0")

    assert tree_order_book.orders == {}


@pytest.mark.parametrize(
    "side, side_of_duplicated_order", [("B", "B"), ("B", "S"), ("S", "B"), ("S", "S")]
)
def test_new_ticker_for_order_with_duplicated_id_should_not_be_added_to_book(
    tree_order_book: TreeOrderBook, side: str, side_of_duplicated_order: str
):
    ticker_of_duplicated_order = "ZZZZ"
    duplicated_id = "X"

    first_order = f"1|{duplicated_id}|a|ZZZY|{side}|8.8|2"
    second_order = f"2|{duplicated_id}|a|{ticker_of_duplicated_order}|{side_of_duplicated_order}|7.7|1"

    process_order(order_book=tree_order_book, order=first_order)
    process_order(order_book=tree_order_book, order=second_order)

    assert ticker_of_duplicated_order not in tree_order_book.orders.keys()


@pytest.mark.parametrize(
    "side, container, order_type",
    [("B", "bids", OrderType.BID), ("S", "asks", OrderType.ASK)],
)
def test_root_should_contain_all_orders_of_same_price(
    tree_order_book: TreeOrderBook, side: str, container: str, order_type: OrderType
):
    ticker = "TICK"
    price = 0.12345

    first_order_id = "X"
    first_size = 100
    first_timestamp = "1000"

    second_order_id = "Y"
    second_size = 200
    second_timestamp = "2000"

    first_order = (
        f"{first_timestamp}|{first_order_id}|a|{ticker}|{side}|{price}|{first_size}"
    )
    second_order = (
        f"{second_timestamp}|{second_order_id}|a|{ticker}|{side}|{price}|{second_size}"
    )

    process_order(order_book=tree_order_book, order=first_order)
    process_order(order_book=tree_order_book, order=second_order)

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
            size=second_size,
            order_type=order_type,
        ),
    }


@pytest.mark.parametrize(
    "side, container, order_type",
    [("B", "bids", OrderType.BID), ("S", "asks", OrderType.ASK)],
)
def test_given_root_with_lower_price_then_right_child_should_contain_all_orders_of_same_higher_price(
    tree_order_book: TreeOrderBook, side: str, container: str, order_type: OrderType
):
    ticker = "TICK"
    price = 0.12345

    first_order_id = "X"
    first_size = 100
    first_timestamp = "1000"

    second_order_id = "Y"
    second_size = 200
    second_timestamp = "2000"

    first_order = (
        f"{first_timestamp}|{first_order_id}|a|{ticker}|{side}|{price}|{first_size}"
    )
    second_order = (
        f"{second_timestamp}|{second_order_id}|a|{ticker}|{side}|{price}|{second_size}"
    )

    process_order(order_book=tree_order_book, order=f"{123}|Z|a|{ticker}|{side}|0.1|1")
    process_order(order_book=tree_order_book, order=first_order)
    process_order(order_book=tree_order_book, order=second_order)

    tree_root = tree_order_book.orders[ticker][container].root
    assert tree_root is not None
    assert tree_root.right.orders == {
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
            size=second_size,
            order_type=order_type,
        ),
    }


@pytest.mark.parametrize(
    "side, container, order_type",
    [("B", "bids", OrderType.BID), ("S", "asks", OrderType.ASK)],
)
def test_given_root_with_lower_price_then_left_child_should_contain_all_orders_of_same_higher_price(
    tree_order_book: TreeOrderBook, side: str, container: str, order_type: OrderType
):
    ticker = "TICK"
    price = 0.12345

    first_order_id = "X"
    first_size = 100
    first_timestamp = "1000"

    second_order_id = "Y"
    second_size = 200
    second_timestamp = "2000"

    first_order = (
        f"{first_timestamp}|{first_order_id}|a|{ticker}|{side}|{price}|{first_size}"
    )
    second_order = (
        f"{second_timestamp}|{second_order_id}|a|{ticker}|{side}|{price}|{second_size}"
    )

    process_order(order_book=tree_order_book, order=f"{123}|Z|a|{ticker}|{side}|9999|1")
    process_order(order_book=tree_order_book, order=first_order)
    process_order(order_book=tree_order_book, order=second_order)

    tree_root = tree_order_book.orders[ticker][container].root
    assert tree_root is not None
    assert tree_root.left.orders == {
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
            size=second_size,
            order_type=order_type,
        ),
    }


@pytest.mark.parametrize(
    "first_order_container, side, side_of_duplicated_order",
    [("bids", "B", "B"), ("bids", "B", "S"), ("asks", "S", "B"), ("asks", "S", "S")],
)
def test_order_with_duplicated_id_should_not_be_added_to_tree_for_given_ticker(
    tree_order_book: TreeOrderBook,
    first_order_container: str,
    side: str,
    side_of_duplicated_order: str,
):
    ticker = "ZZZZ"
    duplicated_id = "X"

    first_order = f"1|{duplicated_id}|a|{ticker}|{side}|8.8|2"
    second_order = f"2|{duplicated_id}|a|{ticker}|{side_of_duplicated_order}|7.7|1"

    process_order(order_book=tree_order_book, order=first_order)
    process_order(order_book=tree_order_book, order=second_order)

    tree_root = tree_order_book.orders[ticker][first_order_container].root
    assert tree_root is not None
    assert tree_root.left is None and tree_root.right is None


@pytest.mark.parametrize(
    "side, side_of_duplicated_order", [("B", "B"), ("B", "S"), ("S", "B"), ("S", "S")]
)
def test_trying_to_add_order_with_duplicated_id_should_log_error(
    tree_order_book: TreeOrderBook, side: str, side_of_duplicated_order: str, capsys
):
    duplicated_id = "aabb1"

    process_order(
        order_book=tree_order_book, order=f"123|{duplicated_id}|a|ZZZY|{side}|8.88888|2"
    )
    process_order(
        order_book=tree_order_book,
        order=f"124|{duplicated_id}|a|ZZZZ|{side_of_duplicated_order}|7.77777|1",
    )

    error_regex = re.compile(f"ERROR.*{duplicated_id}")
    assert error_regex.match(capsys.readouterr().err)
