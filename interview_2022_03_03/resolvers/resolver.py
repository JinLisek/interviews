from abc import ABC, abstractmethod
from typing import Dict, List

Signal = str
Signals = List[Signal]
Value = int
CalculatedSignals = Dict[Signal, Value]


class Resolver(ABC):
    @abstractmethod
    def get_input_signals(self) -> Signals:
        pass

    @abstractmethod
    def get_output_signals(self) -> Signals:
        pass

    @abstractmethod
    def run(self, known_signals: CalculatedSignals) -> CalculatedSignals:
        pass
