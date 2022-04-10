from interview_2022_03_28 import order_processing

from ._check_perf import check_perf
from ._helpers import SideSelector, TickerSelector, add_order, describe_price_test

NUM_OF_ADDITIONS = 100_000
NUM_OF_PRICE_API_CALLS = 100


def prepare_orders_before_test(
    processor: order_processing.OrderBookProcessor, ticker_selector: TickerSelector
) -> None:
    side_selector = SideSelector()
    for idx in range(NUM_OF_ADDITIONS):
        add_order(
            processor=processor, idx=idx, side=side_selector(), ticker=ticker_selector()
        )


def multiple_tickers_best_price() -> None:
    describe_price_test(
        name="multiple_tickers_best_price",
        price_api_calls=NUM_OF_PRICE_API_CALLS,
        orders=NUM_OF_ADDITIONS,
    )
    order_database = order_processing.create_order_database(name=":memory:")
    order_storage = order_processing.create_order_storage(database=order_database)
    order_viewer = order_storage.get_price_view()
    ticker_selector = TickerSelector()
    print("Preparing orders before test")
    prepare_orders_before_test(
        processor=order_storage.get_processor(), ticker_selector=ticker_selector
    )
    print("Orders prepared, starting test")

    with check_perf():
        for _ in range(NUM_OF_PRICE_API_CALLS):
            order_processing.get_best_bid_and_ask(
                order_book=order_viewer, ticker=ticker_selector()
            )


if __name__ == "__main__":
    multiple_tickers_best_price()
