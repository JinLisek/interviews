from interview_2022_03_28 import order_processing

from ._check_perf import check_perf
from ._helpers import SideSelector, TickerSelector, add_order, describe_test

NUM_OF_ADDITIONS = 450_000


def multiple_tickers_only_additions() -> None:
    describe_test(
        name="multiple_tickers_only_additions",
        additions=NUM_OF_ADDITIONS,
        updates=0,
        cancels=0,
    )

    order_storage = order_processing.create_db_order_storage()
    order_processor = order_storage.get_processor()
    side_selector = SideSelector()
    ticker_selector = TickerSelector()

    with check_perf():
        for idx in range(NUM_OF_ADDITIONS):
            add_order(
                processor=order_processor,
                idx=idx,
                side=side_selector(),
                ticker=ticker_selector(),
            )


if __name__ == "__main__":
    multiple_tickers_only_additions()
