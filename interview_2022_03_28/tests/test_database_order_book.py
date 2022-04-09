import pytest

from ..concrete_order_database import ConcreteOrderDatabase
from ..database_order_book import DatabaseOrderBook, DuplicatedOrderIdError
from ..order import Order


@pytest.fixture(name="temporary_database")
def fixture_temporary_database():
    return ConcreteOrderDatabase(database_name=":memory:")


@pytest.fixture(name="object_under_test")
def fixture_object_under_test(temporary_database):
    return DatabaseOrderBook(database=temporary_database)


def create_tuple_from_order(order: Order) -> tuple:
    return (order.order_id, order.ticker, order.price, order.size)


def test_given_ask_then_order_should_be_added(object_under_test, temporary_database):
    order = Order(order_id=1, ticker="2222", price=3.3, size=4)
    object_under_test.ask(order=order)

    assert temporary_database.fetch_orders() == [create_tuple_from_order(order=order)]


def test_given_bid_then_order_should_be_added(object_under_test, temporary_database):
    order = Order(order_id=1, ticker="2222", price=3.3, size=4)
    object_under_test.bid(order=order)

    assert temporary_database.fetch_orders() == [create_tuple_from_order(order=order)]


def test_given_ask_with_duplicated_order_id_then_should_raise(
    object_under_test,
):
    duplicated_order_id = 8
    ticker = "TICK"
    object_under_test.ask(
        order=Order(order_id=duplicated_order_id, ticker=ticker, price=2.2, size=1)
    )

    with pytest.raises(DuplicatedOrderIdError):
        object_under_test.ask(
            order=Order(order_id=duplicated_order_id, ticker=ticker, price=3.3, size=1)
        )


def test_given_ask_with_size_zero_then_it_should_not_be_added(
    object_under_test, temporary_database
):
    object_under_test.ask(order=Order(order_id=777, ticker="TICK", price=1.1, size=0))

    assert temporary_database.fetch_orders() == []


def test_given_ask_with_price_zero_then_it_should_be_added(
    object_under_test, temporary_database
):
    order = Order(order_id=777, ticker="TICK", price=0.0, size=22)
    object_under_test.ask(order=order)

    assert temporary_database.fetch_orders() == [create_tuple_from_order(order)]


def test_given_no_asks_then_best_ask_should_be_zero(object_under_test):
    assert object_under_test.get_best_ask(ticker="TICK") == pytest.approx(0)


def test_given_ask_for_tic1_then_best_ask_for_tic2_should_be_zero(object_under_test):
    object_under_test.ask(
        order=Order(order_id=777, ticker="TIC1", price=123.45678, size=100)
    )

    assert object_under_test.get_best_ask(ticker="TIC2") == pytest.approx(0)


def test_given_single_ask_then_best_ask_should_be_that_ask(object_under_test):
    ticker = "AAPL"
    ask_price = 1.00001
    object_under_test.ask(
        order=Order(order_id=8, ticker=ticker, price=ask_price, size=100)
    )

    assert object_under_test.get_best_ask(ticker=ticker) == pytest.approx(ask_price)


def test_given_two_asks_with_best_being_second_then_best_ask_should_be_the_second_ask(
    object_under_test,
):
    ticker = "AAPL"
    best_price = 3.3
    object_under_test.ask(order=Order(order_id=8, ticker=ticker, price=88.8, size=100))
    object_under_test.ask(
        order=Order(order_id=2, ticker=ticker, price=best_price, size=100)
    )

    assert object_under_test.get_best_ask(ticker=ticker) == pytest.approx(best_price)


def test_given_two_asks_with_best_being_first_then_best_ask_should_be_the_first_ask(
    object_under_test,
):
    ticker = "AAPL"
    best_price = 4.4
    object_under_test.ask(
        order=Order(order_id=8, ticker=ticker, price=best_price, size=100)
    )
    object_under_test.ask(order=Order(order_id=9, ticker=ticker, price=99.9, size=100))

    assert object_under_test.get_best_ask(ticker=ticker) == pytest.approx(best_price)


def test_after_cancelling_the_only_order_should_be_no_more_asks(object_under_test):
    ticker = "TICK"
    order_id = 77

    object_under_test.ask(
        order=Order(order_id=order_id, ticker=ticker, price=12.34, size=1)
    )
    object_under_test.cancel(order_id=order_id)

    assert object_under_test.get_best_ask(ticker=ticker) == pytest.approx(0)


def test_after_cancelling_order_with_best_ask_then_get_best_ask_should_return_new_best(
    object_under_test,
):
    ticker = "TICK"
    best_ask_order_id = 17
    second_best_ask_price = 99

    object_under_test.ask(
        order=Order(order_id=best_ask_order_id, ticker=ticker, price=12.34, size=1)
    )
    object_under_test.ask(
        order=Order(order_id=2, ticker=ticker, price=second_best_ask_price, size=1)
    )
    object_under_test.cancel(order_id=best_ask_order_id)

    assert object_under_test.get_best_ask(ticker=ticker) == pytest.approx(
        second_best_ask_price
    )


def test_blax_can_update(object_under_test):
    ticker = "TICK"
    order_id = 17

    object_under_test.ask(
        order=Order(order_id=order_id, ticker=ticker, price=12.34, size=1)
    )
    object_under_test.update(order_id=order_id, size=2)
