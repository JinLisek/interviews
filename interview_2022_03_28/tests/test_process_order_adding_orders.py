import re

import pytest

from ..process_order import process_order


@pytest.mark.usefixtures("order_book")
def test_orders_should_be_empty_by_default(database):
    assert database.fetch_orders() == []


@pytest.mark.parametrize("side", ["B", "S"])
def test_after_adding_order_there_should_be_one_order(order_book, database, side):
    process_order(order_book=order_book, order=f"123|z42|a|ZZZZ|{side}|7.77777|1")

    assert len(database.fetch_orders()) == 1


@pytest.mark.parametrize("side", ["B", "S"])
def test_after_adding_order_then_timestamp_should_be_added_to_order(
    order_book, database, side
):
    added_timestamp = 12345
    process_order(
        order_book=order_book,
        order=f"{added_timestamp}|a42|a|ZZZZ|{side}|7.77777|1",
    )

    assert added_timestamp in database.fetch_orders()[0]


@pytest.mark.parametrize("side", ["B", "S"])
def test_after_adding_order_then_order_id_should_be_added_to_order(
    order_book, database, side
):
    order_id = "abbb11"
    process_order(
        order_book=order_book, order=f"123|{order_id}|a|ZZZZ|{side}|7.77777|1"
    )

    assert order_id in database.fetch_orders()[0]


@pytest.mark.parametrize("side", ["B", "S"])
def test_after_adding_order_then_ticker_should_be_added_to_order(
    order_book, database, side
):
    ticker = "AAPL"
    process_order(order_book=order_book, order=f"123|a42|a|{ticker}|{side}|7.77777|1")

    assert ticker in database.fetch_orders()[0]


@pytest.mark.parametrize("side", ["B", "S"])
def test_after_adding_order_then_price_should_be_added_to_order(
    order_book, database, side
):
    price = 89.12345
    process_order(order_book=order_book, order=f"123|a42|a|ZZZZ|{side}|{price}|1")

    assert price in database.fetch_orders()[0]


@pytest.mark.parametrize("side", ["B", "S"])
def test_after_adding_order_then_size_should_be_added_to_order(
    order_book, database, side
):
    size = 1337
    process_order(order_book=order_book, order=f"123|a42|a|ZZZZ|{side}|7.77777|{size}")

    assert size in database.fetch_orders()[0]


def test_after_adding_sell_order_then_order_should_be_marked_with_ask(
    order_book, database
):
    process_order(order_book=order_book, order="123|a42|a|ZZZZ|S|7.77777|1")

    assert "ASK" in database.fetch_orders()[0]


def test_after_adding_buy_order_then_order_should_be_marked_with_bid(
    order_book, database
):
    process_order(order_book=order_book, order="123|a42|a|ZZZZ|B|7.77777|1")

    assert "BID" in database.fetch_orders()[0]


def test_after_adding_two_orders_database_should_contain_two_orders(
    order_book, database
):
    process_order(order_book=order_book, order="123|z42|a|ZZZZ|B|7.77777|1")
    process_order(order_book=order_book, order="123|z44|a|ZZZZ|S|7.77777|1")

    assert len(database.fetch_orders()) == 2


def test_after_adding_two_orders_database_should_orders_with_different_ids(
    order_book, database
):
    process_order(order_book=order_book, order="123|z42|a|ZZZZ|B|7.77777|1")
    process_order(order_book=order_book, order="123|z44|a|ZZZZ|S|7.77777|1")

    orders = database.fetch_column(column="order_id")
    assert orders[0] != orders[1]


def test_order_with_size_zero_should_not_be_added_to_database(order_book, database):
    process_order(order_book=order_book, order="123|a42|a|ZZZZ|X|7.77777|0")

    assert database.fetch_orders() == []


def test_order_with_incorrect_side_should_not_be_added_to_database(
    order_book, database
):
    process_order(order_book=order_book, order="123|a42|a|ZZZZ|X|7.77777|1")

    assert database.fetch_orders() == []


def test_order_with_duplicated_id_should_not_be_added_to_database(order_book, database):
    process_order(order_book=order_book, order="124|z42|a|ZZZY|B|8.88888|2")
    process_order(order_book=order_book, order="123|z42|a|ZZZZ|S|7.77777|1")

    assert len(database.fetch_orders()) == 1


def test_trying_to_add_order_with_duplicated_id_should_log_error(order_book, capsys):
    duplicated_id = "aabb1"

    process_order(
        order_book=order_book, order=f"123|{duplicated_id}|a|ZZZY|B|8.88888|2"
    )
    process_order(
        order_book=order_book, order=f"124|{duplicated_id}|a|ZZZZ|S|7.77777|1"
    )

    error_regex = re.compile(f"ERROR.*{duplicated_id}")
    assert error_regex.match(capsys.readouterr().err)
