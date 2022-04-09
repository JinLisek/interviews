from abc import ABC, abstractmethod

from .order import Order


class OrderBookError(Exception):
    pass


class OrderBookProcessor(ABC):
    @abstractmethod
    def add_order(self, order: Order) -> None:
        pass

    @abstractmethod
    def cancel(self, order_id: str) -> None:
        pass

    @abstractmethod
    def update(self, order_id: str, size: int) -> None:
        pass
