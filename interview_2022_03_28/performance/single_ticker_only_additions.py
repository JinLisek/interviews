from interview_2022_03_28 import order_processing

from ._check_perf import check_perf
from ._helpers import SideSelector, add_order, describe_test

NUM_OF_ADDITIONS = 450_000


def single_ticker_only_additions() -> None:
    describe_test(
        name="single_ticker_only_additions",
        additions=NUM_OF_ADDITIONS,
        updates=0,
        cancels=0,
    )
    order_database = order_processing.create_order_database(name=":memory:")
    order_storage = order_processing.create_order_storage(database=order_database)
    order_processor = order_storage.get_processor()
    side_selector = SideSelector()

    with check_perf():
        for idx in range(NUM_OF_ADDITIONS):
            add_order(
                processor=order_processor, idx=idx, side=side_selector(), ticker="AAPL"
            )


if __name__ == "__main__":
    single_ticker_only_additions()
