import pytest
from interview_2022_03_03.resolvers import CalculatedSignals, Resolver, Signals

from .._concrete_engines import RegularResolvingEngine
from ..exceptions import MissingResolverError


class AToBResolverStub(Resolver):
    def get_input_signals(self) -> Signals:
        return ["A"]

    def get_output_signals(self) -> Signals:
        return ["B"]

    def run(self, known_signals: CalculatedSignals) -> CalculatedSignals:
        return {"B": known_signals["A"] + 1}


class BToCResolverStub(Resolver):
    def get_input_signals(self) -> Signals:
        return ["B"]

    def get_output_signals(self) -> Signals:
        return ["C"]

    def run(self, known_signals: CalculatedSignals) -> CalculatedSignals:
        return {"C": known_signals["B"] + 10}


class CToDResolverStub(Resolver):
    def get_input_signals(self) -> Signals:
        return ["C"]

    def get_output_signals(self) -> Signals:
        return ["D"]

    def run(self, known_signals: CalculatedSignals) -> CalculatedSignals:
        return {"D": known_signals["C"] + 100}


class SumAAndBResolverStub(Resolver):
    def get_input_signals(self) -> Signals:
        return ["A", "B"]

    def get_output_signals(self) -> Signals:
        return ["A+B"]

    def run(self, known_signals: CalculatedSignals) -> CalculatedSignals:
        return {"A+B": known_signals["A"] + known_signals["B"]}


class DoubleAndHalfAResolverStub(Resolver):
    def get_input_signals(self) -> Signals:
        return ["A"]

    def get_output_signals(self) -> Signals:
        return ["DoubleA", "HalfA"]

    def run(self, known_signals: CalculatedSignals) -> CalculatedSignals:
        return {"DoubleA": known_signals["A"] * 2, "HalfA": known_signals["A"] // 2}


class XIsAYIsBResolverStub(Resolver):
    def get_input_signals(self) -> Signals:
        return ["A", "B"]

    def get_output_signals(self) -> Signals:
        return ["X", "Y"]

    def run(self, known_signals: CalculatedSignals) -> CalculatedSignals:
        return {"X": known_signals["A"], "Y": known_signals["B"]}


def test_given_lookup_in_known_signals_should_return_known_signals():
    engine = RegularResolvingEngine()

    input_signals = {"A": 777}

    assert input_signals == engine.resolve(
        lookup_signal="A", known_signals=input_signals
    )


def test_given_multiple_resolvers_depending_on_each_other_should_calculate():
    engine = RegularResolvingEngine()

    engine.register_resolver(resolver=AToBResolverStub())
    engine.register_resolver(resolver=BToCResolverStub())
    engine.register_resolver(resolver=CToDResolverStub())

    input_signals = {"A": 0}

    assert {**input_signals, "B": 1, "C": 11, "D": 111} == engine.resolve(
        lookup_signal="D", known_signals=input_signals
    )


def test_given_resolver_requiring_multiple_input_should_calculate_single_output():
    engine = RegularResolvingEngine()

    engine.register_resolver(resolver=SumAAndBResolverStub())

    input_signals = {"A": 3, "B": 5}

    assert {**input_signals, "A+B": 8} == engine.resolve(
        lookup_signal="A+B", known_signals=input_signals
    )


@pytest.mark.parametrize(("lookup_signal"), (["DoubleA", "HalfA"]))
def test_given_resolver_requiring_single_input_should_calculate_multiple_outputs(
    lookup_signal,
):
    engine = RegularResolvingEngine()

    engine.register_resolver(resolver=DoubleAndHalfAResolverStub())

    input_signals = {"A": 9}

    assert {**input_signals, "DoubleA": 18, "HalfA": 4} == engine.resolve(
        lookup_signal=lookup_signal, known_signals=input_signals
    )


def test_given_resolver_requiring_multiple_input_should_calculate_multiple_outputs():
    engine = RegularResolvingEngine()

    engine.register_resolver(resolver=XIsAYIsBResolverStub())

    a_value = 49
    b_value = 51

    input_signals = {"A": a_value, "B": b_value}

    assert {**input_signals, "X": a_value, "Y": b_value} == engine.resolve(
        lookup_signal="X", known_signals=input_signals
    )


def test_when_no_resolver_given_for_lookup_signal_should_raise_an_error():
    engine = RegularResolvingEngine()

    missing_signal = "ComplexMissingSignalName42"

    with pytest.raises(MissingResolverError) as err:
        engine.resolve(lookup_signal=missing_signal, known_signals={"A": 10})

    assert missing_signal in str(err)
