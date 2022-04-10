from interview_2022_03_28 import order_processing

from ._check_perf import check_perf
from ._helpers import SideSelector, add_order, cancel_order, describe_test, update_order

OPERATIONS = 150_000


def single_ticker_additions_updates_cancels() -> None:
    describe_test(
        name="single_ticker_additions_updates_cancels",
        additions=OPERATIONS,
        updates=OPERATIONS,
        cancels=OPERATIONS,
    )
    order_database = order_processing.create_order_database(name=":memory:")
    order_storage = order_processing.create_order_storage(database=order_database)
    order_processor = order_storage.get_processor()
    side_selector = SideSelector()

    with check_perf():
        for idx in range(OPERATIONS):
            add_order(
                processor=order_processor, idx=idx, side=side_selector(), ticker="AAPL"
            )
            update_order(processor=order_processor, idx=idx)
            cancel_order(processor=order_processor, idx=idx)


if __name__ == "__main__":
    single_ticker_additions_updates_cancels()
