from interview_2022_03_28 import order_processing

from ._check_perf import check_perf
from ._helpers import (
    SideSelector,
    TickerSelector,
    add_order,
    cancel_order,
    describe_test,
    update_order,
)

OPERATIONS = 150_000


def multiple_tickers_additions_updates_cancels() -> None:
    describe_test(
        name="multiple_tickers_additions_updates_cancels",
        additions=OPERATIONS,
        updates=OPERATIONS,
        cancels=OPERATIONS,
    )
    order_storage = order_processing.create_db_order_storage()
    order_processor = order_storage.get_processor()
    side_selector = SideSelector()
    ticker_selector = TickerSelector()

    with check_perf():
        for idx in range(OPERATIONS):
            add_order(
                processor=order_processor,
                idx=idx,
                side=side_selector(),
                ticker=ticker_selector(),
            )
            update_order(processor=order_processor, idx=idx)
            cancel_order(processor=order_processor, idx=idx)


if __name__ == "__main__":
    multiple_tickers_additions_updates_cancels()
