from .best_bid_and_ask_view import BestBidAndAskView
from .database_order_book import DatabaseOrderBook
from .order_book import OrderBookProcessor
from .order_database import OrderDatabase
from .order_storage import OrderStorage


class ConcreteOrderStorage(OrderStorage):
    def __init__(self, database: OrderDatabase) -> None:
        self.__order_book = DatabaseOrderBook(database=database)

    def get_processor(self) -> OrderBookProcessor:
        return self.__order_book

    def get_price_view(self) -> BestBidAndAskView:
        return self.__order_book