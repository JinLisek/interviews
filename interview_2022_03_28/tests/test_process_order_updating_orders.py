import re

from ..process_order import process_order


def test_given_empty_database_updating_order_should_not_add_orders(
    order_book, database
):
    process_order(order_book=order_book, order="456|1o1|u|20")

    assert database.fetch_orders() == []


def test_given_empty_database_updating_order_should_log_error(order_book, capsys):
    order_id = "1o1"
    process_order(order_book=order_book, order=f"456|{order_id}|u|20")

    error_regex = re.compile(f"ERROR.*{order_id}")
    assert error_regex.match(capsys.readouterr().err)


def test_updating_non_existing_order_should_not_modify_other_orders(
    order_book, database
):
    id_of_updated_order = "updated"

    timestamp = "789"
    id_of_unchanging_order = "bbaa"
    ticker = "XXYY"
    price = 4.56789
    size = 8

    process_order(
        order_book=order_book,
        order=f"{timestamp}|{id_of_unchanging_order}|a|{ticker}|B|{price}|{size}",
    )

    process_order(
        order_book=order_book, order=f"456|{id_of_updated_order}|a|DDEE|B|1.2|3"
    )
    process_order(order_book=order_book, order=f"456|{id_of_updated_order}|u|20")

    assert (
        id_of_unchanging_order,
        int(timestamp),
        ticker,
        price,
        size,
        "BID",
    ) in database.fetch_orders()


def test_updating_existing_order_should_change_its_size(order_book, database):
    order_id = "bbaa"
    new_size = 88
    process_order(order_book=order_book, order=f"789|{order_id}|a|SCRUB|B|1.2|1")
    process_order(order_book=order_book, order=f"789|{order_id}|u|{new_size}")

    assert (new_size,) in database.fetch_column(column="size")


def test_updating_existing_order_should_not_modify_other_orders(order_book, database):
    id_of_updated_order = "upd11"

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
        order_book=order_book, order=f"789|{id_of_updated_order}|a|SCRUB|B|1.2|1"
    )
    process_order(order_book=order_book, order=f"789|{id_of_updated_order}|u|1001")

    assert (
        id_of_unchanged_order,
        int(timestamp),
        ticker,
        price,
        size,
        "BID",
    ) in database.fetch_orders()


def test_updating_existing_order_should_not_modify_num_of_orders(order_book, database):
    id_of_updated_order = "upd11"

    process_order(order_book=order_book, order="123|unchanged|a|AABB|B|1.1|1")
    process_order(
        order_book=order_book, order=f"789|{id_of_updated_order}|a|SCRUB|B|1.2|1"
    )
    process_order(order_book=order_book, order=f"789|{id_of_updated_order}|u|1001")

    assert len(database.fetch_orders()) == 2
