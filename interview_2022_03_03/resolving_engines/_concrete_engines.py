from typing import Dict

from .engine import CalculatedSignals, Resolver, ResolvingEngine, Signal
from .exceptions import MissingResolverError


class RegularResolvingEngine(ResolvingEngine):
    def __init__(self) -> None:
        self.__resolvers: Dict[Signal, Resolver] = {}

    def register_resolver(self, resolver: Resolver) -> None:
        for signal in resolver.get_output_signals():
            self.__resolvers[signal] = resolver

    def resolve(
        self, lookup_signal: Signal, known_signals: CalculatedSignals
    ) -> CalculatedSignals:
        if lookup_signal in known_signals:
            return known_signals

        try:
            resolver = self.__resolvers[lookup_signal]
        except KeyError as err:
            raise MissingResolverError(
                f"Missing resolver for signal: {lookup_signal}"
            ) from err

        for signal in resolver.get_input_signals():
            if signal not in known_signals:
                self.resolve(lookup_signal=signal, known_signals=known_signals)

        known_signals.update(resolver.run(known_signals=known_signals))

        return known_signals
