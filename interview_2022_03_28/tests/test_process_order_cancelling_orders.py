import re

from ..process_order import process_order


def test_cancelling_order_with_empty_database_should_not_add_orders(
    order_book, database
):
    process_order(order_book=order_book, order="789|e11|c")

    assert database.fetch_orders() == []


def test_cancelling_non_existing_order_should_not_modify_existing_orders(
    order_book, database
):
    timestamp = "789"
    order_id = "bbaa"
    ticker = "XXYY"
    price = 4.56789
    size = 8
    process_order(
        order_book=order_book,
        order=f"{timestamp}|{order_id}|a|{ticker}|B|{price}|{size}",
    )
    process_order(order_book=order_book, order="789|e11|c")

    assert database.fetch_orders() == [
        (order_id, int(timestamp), ticker, price, size, "BID")
    ]


def test_cancelling_non_existing_order_should_log_error(order_book, capsys):
    order_id = "123lol"
    process_order(order_book=order_book, order=f"789|{order_id}|c")

    error_regex = re.compile(f"ERROR.*{order_id}")
    assert error_regex.match(capsys.readouterr().err)


def test_cancelling_existing_order_should_remove_it_from_database(order_book, database):
    order_id = "bbaa"
    process_order(order_book=order_book, order=f"789|{order_id}|a|SCRUB|B|1.2|1")
    process_order(order_book=order_book, order=f"789|{order_id}|c")

    assert database.fetch_orders() == []


def test_cancelling_existing_order_should_not_modify_other_orders(order_book, database):
    order_id_to_cancel = "cancelled"

    timestamp = "789"
    id_of_unchanged_order = "bbaa"
    ticker = "XXYY"
    price = 4.56789
    size = 8

    process_order(
        order_book=order_book,
        order=f"{timestamp}|{id_of_unchanged_order}|a|{ticker}|B|{price}|{size}",
    )
    process_order(
        order_book=order_book, order=f"789|{order_id_to_cancel}|a|SCRUB|B|1.2|1"
    )
    process_order(order_book=order_book, order=f"789|{order_id_to_cancel}|c")

    assert database.fetch_orders() == [
        (id_of_unchanged_order, int(timestamp), ticker, price, size, "BID")
    ]
