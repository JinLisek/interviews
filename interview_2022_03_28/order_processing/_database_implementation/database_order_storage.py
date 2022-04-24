from ..best_bid_and_ask_view import BestBidAndAskView
from ..order_book import OrderBookProcessor
from ..order_storage import OrderStorage
from .database_order_book import DatabaseOrderBook
from .order_database import OrderDatabase


class DatabaseOrderStorage(OrderStorage):
    def __init__(self, database: OrderDatabase) -> None:
        self.__order_book = DatabaseOrderBook(database=database)

    def get_processor(self) -> OrderBookProcessor:
        return self.__order_book

    def get_price_view(self) -> BestBidAndAskView:
        return self.__order_book
