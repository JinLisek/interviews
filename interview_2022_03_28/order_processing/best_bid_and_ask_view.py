from abc import ABC, abstractmethod


class BestBidAndAskView(ABC):
    @abstractmethod
    def get_best_ask(self, ticker: str) -> float:
        pass

    @abstractmethod
    def get_best_bid(self, ticker: str) -> float:
        pass
