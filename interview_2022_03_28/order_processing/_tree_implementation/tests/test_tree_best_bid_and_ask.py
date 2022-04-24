import pytest

from ...best_bid_and_ask import get_best_bid_and_ask
from ...order import Order, OrderType
from ..tree_order_book import TreeOrderBook


def create_ask(order_id: str, ticker: str, price: float) -> Order:
    return Order(
        order_id=order_id,
        timestamp="2",
        ticker=ticker,
        price=price,
        size=1,
        order_type=OrderType.ASK,
    )


def create_bid(order_id: str, ticker: str, price: float) -> Order:
    return Order(
        order_id=order_id,
        timestamp="23",
        ticker=ticker,
        price=price,
        size=1,
        order_type=OrderType.BID,
    )


@pytest.mark.parametrize("check_type", ["best_ask", "best_bid"])
def test_given_non_existing_ticker_should_return_zero(
    tree_order_book: TreeOrderBook, check_type: str
):
    result = get_best_bid_and_ask(order_book=tree_order_book, ticker="NONEXT")
    assert result[check_type] == pytest.approx(0)


def test_given_single_bid_then_should_return_its_price_as_best_bid(
    tree_order_book: TreeOrderBook,
):
    ticker = "TICK"
    bid_price = 97.00001

    tree_order_book.add_order(
        order=create_bid(order_id="1", ticker=ticker, price=bid_price)
    )

    result = get_best_bid_and_ask(order_book=tree_order_book, ticker=ticker)
    assert result["best_bid"] == pytest.approx(bid_price)


def test_given_single_ask_then_should_return_its_price_as_best_ask(
    tree_order_book: TreeOrderBook,
):
    ticker = "TICK"
    ask_price = 97.00001

    tree_order_book.add_order(
        order=create_ask(order_id="2", ticker=ticker, price=ask_price)
    )

    result = get_best_bid_and_ask(order_book=tree_order_book, ticker=ticker)
    assert result["best_ask"] == pytest.approx(ask_price)


def test_given_single_bid_then_should_best_ask_should_be_zero(
    tree_order_book: TreeOrderBook,
):
    ticker = "TICK"

    tree_order_book.add_order(
        order=create_bid(order_id="3", ticker=ticker, price=13.37)
    )

    result = get_best_bid_and_ask(order_book=tree_order_book, ticker=ticker)
    assert result["best_ask"] == pytest.approx(0)


def test_given_single_ask_then_should_best_bid_should_be_zero(
    tree_order_book: TreeOrderBook,
):
    ticker = "TICK"

    tree_order_book.add_order(
        order=create_ask(order_id="4", ticker=ticker, price=13.37)
    )

    result = get_best_bid_and_ask(order_book=tree_order_book, ticker=ticker)
    assert result["best_bid"] == pytest.approx(0)


def test_given_multiple_asks_then_should_return_lowest_price_as_best_ask(
    tree_order_book: TreeOrderBook,
):
    ticker = "TICK"
    lowest_price = 1.1

    tree_order_book.add_order(order=create_ask(order_id="1", ticker=ticker, price=8.8))
    tree_order_book.add_order(
        order=create_ask(order_id="2", ticker=ticker, price=lowest_price)
    )
    tree_order_book.add_order(order=create_ask(order_id="3", ticker=ticker, price=7.7))

    result = get_best_bid_and_ask(order_book=tree_order_book, ticker=ticker)
    assert result["best_ask"] == pytest.approx(lowest_price)


def test_given_multiple_bids_then_should_return_highest_price_as_best_bid(
    tree_order_book: TreeOrderBook,
):
    ticker = "TICK"
    highest_price = 77.77

    tree_order_book.add_order(order=create_bid(order_id="1", ticker=ticker, price=6.6))
    tree_order_book.add_order(
        order=create_bid(order_id="2", ticker=ticker, price=highest_price)
    )
    tree_order_book.add_order(order=create_bid(order_id="3", ticker=ticker, price=5.5))

    result = get_best_bid_and_ask(order_book=tree_order_book, ticker=ticker)
    assert result["best_bid"] == pytest.approx(highest_price)
