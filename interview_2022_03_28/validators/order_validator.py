from __future__ import annotations

from abc import ABC, abstractmethod


class OrderValidator(ABC):
    @abstractmethod
    def is_valid(self, order: str) -> bool:
        pass

    @abstractmethod
    def set_next(self, validator: OrderValidator) -> OrderValidator:
        pass
