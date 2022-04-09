from typing import Dict

from .order_book import DatabaseOrderBook

Ticker = str
Price = float


def get_best_bid_and_ask(
    order_book: DatabaseOrderBook, ticker: Ticker
) -> Dict[Ticker, Price]:
    return {
        "best_ask": order_book.get_best_ask(ticker=ticker),
        "best_bid": order_book.get_best_bid(ticker=ticker),
    }
