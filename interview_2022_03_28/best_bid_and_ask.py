from typing import Dict

from .best_bid_and_ask_view import BestBidAndAskView

Ticker = str
Price = float


def get_best_bid_and_ask(
    order_book: BestBidAndAskView, ticker: Ticker
) -> Dict[Ticker, Price]:
    return {
        "best_ask": order_book.get_best_ask(ticker=ticker),
        "best_bid": order_book.get_best_bid(ticker=ticker),
    }
