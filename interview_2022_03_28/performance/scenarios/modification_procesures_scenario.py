from interview_2022_03_28 import order_processing

from .._check_perf import check_perf
from .._helpers import (
    SideSelector,
    TickerSelector,
    add_order,
    cancel_order,
    describe_test,
    update_order,
)


def run_modification_procesures_scenario(
    test_name: str,
    storage: order_processing.OrderStorage,
    num_of_additions: int,
    num_of_updates: int,
    num_of_cancels: int,
    num_of_tickers: int,
) -> None:
    if num_of_updates > num_of_additions:
        raise RuntimeError("Num of updates should be <= than num of additions")

    if num_of_cancels > num_of_additions:
        raise RuntimeError("Num of cancels should be <= than num of additions")

    describe_test(
        name=test_name,
        additions=num_of_additions,
        updates=num_of_updates,
        cancels=num_of_cancels,
        num_of_tickers=num_of_tickers,
    )

    order_processor = storage.get_processor()
    side_selector = SideSelector()
    ticker_selector = TickerSelector(num_of_tickers=num_of_tickers)

    with check_perf():
        for idx in range(num_of_additions):
            add_order(
                processor=order_processor,
                idx=idx,
                side=side_selector(),
                ticker=ticker_selector(),
            )

        for idx in range(num_of_updates):
            update_order(processor=order_processor, idx=idx)

        for idx in range(num_of_cancels):
            cancel_order(processor=order_processor, idx=idx)
