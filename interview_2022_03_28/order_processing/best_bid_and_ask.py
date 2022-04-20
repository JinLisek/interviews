from typing import Dict

from .best_bid_and_ask_view import BestBidAndAskView


def get_best_bid_and_ask(
    order_book: BestBidAndAskView, ticker: str
) -> Dict[str, float]:
    return {
        "best_ask": order_book.get_best_ask(ticker=ticker),
        "best_bid": order_book.get_best_bid(ticker=ticker),
    }
