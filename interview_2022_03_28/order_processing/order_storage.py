from abc import ABC, abstractmethod

from .best_bid_and_ask_view import BestBidAndAskView
from .order_book import OrderBookProcessor


class OrderStorage(ABC):
    @abstractmethod
    def get_processor(self) -> OrderBookProcessor:
        pass

    @abstractmethod
    def get_price_view(self) -> BestBidAndAskView:
        pass
