import pytest

from ..process_order import process_order

INCORRECT_INPUTS = [
    "",
    "kugeakufgauk",
    "456|id1",
    "456|id1|",
    "123|z42|INCORRECT-ACTION|ZZZZ|B|7.77777|1",
    "123|z42|u",
    "123|z42|u|",
    "123|z42|u|a",
    "123|z42|u|1a",
    "123|z42|u|a1",
    "123|z42|u|0",
    "123|z42|u|-1",
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
]


@pytest.mark.parametrize("incorrect_order", INCORRECT_INPUTS)
def test_given_incorrect_order_should_log_error(order_book, capsys, incorrect_order):
    process_order(order_book=order_book, order=incorrect_order)

    assert "ERROR" in capsys.readouterr().err


@pytest.mark.parametrize("incorrect_order", INCORRECT_INPUTS)
def test_given_incorrect_order_should_not_add_orders(
    order_book, database, incorrect_order
):
    process_order(order_book=order_book, order=incorrect_order)

    assert database.fetch_orders() == []


@pytest.mark.parametrize("incorrect_order", INCORRECT_INPUTS)
def test_given_incorrect_order_should_not_modify_existing_orders(
    order_book, database, incorrect_order
):
    timestamp = "123"
    order_id = "correct_id"
    ticker = "KCIT"
    price = 8.54321
    size = 17

    process_order(
        order_book=order_book,
        order=f"{timestamp}|{order_id}|a|{ticker}|B|{price}|{size}",
    )
    process_order(order_book=order_book, order=incorrect_order)

    assert (
        order_id,
        int(timestamp),
        ticker,
        price,
        size,
        "BID",
    ) in database.fetch_orders()
