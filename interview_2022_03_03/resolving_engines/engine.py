from abc import ABC, abstractmethod

from interview_2022_03_03.resolvers import CalculatedSignals, Resolver, Signal


class ResolvingEngine(ABC):
    @abstractmethod
    def register_resolver(self, resolver: Resolver) -> None:
        pass

    @abstractmethod
    def resolve(
        self, lookup_signal: Signal, known_signals: CalculatedSignals
    ) -> CalculatedSignals:
        pass
