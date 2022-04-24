from ..best_bid_and_ask_view import BestBidAndAskView
from ..order_book import OrderBookProcessor
from ..order_storage import OrderStorage
from .tree_order_book import TreeOrderBook


class TreeOrderStorage(OrderStorage):
    def __init__(self) -> None:
        self.__order_book = TreeOrderBook()

    def get_processor(self) -> OrderBookProcessor:
        return self.__order_book

    def get_price_view(self) -> BestBidAndAskView:
        return self.__order_book
