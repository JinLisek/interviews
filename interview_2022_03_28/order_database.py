from abc import ABC, abstractmethod

from .order import Order


class OrderDatabase(ABC):
    @abstractmethod
    def create_table(self, name: str, columns) -> None:
        pass

    @abstractmethod
    def insert(self, order: Order) -> None:
        pass

    @abstractmethod
    def remove(self, order_id: str) -> None:
        pass

    @abstractmethod
    def has_order(self, order_id: str) -> bool:
        pass

    @abstractmethod
    def update(self, order_id: str, size: int) -> None:
        pass

    @abstractmethod
    def get_best_ask(self, ticker: str) -> float:
        pass

    @abstractmethod
    def get_best_bid(self, ticker: str) -> float:
        pass
