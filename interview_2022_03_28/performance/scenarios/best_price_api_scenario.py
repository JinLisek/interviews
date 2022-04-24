from interview_2022_03_28 import order_processing

from .._check_perf import check_perf
from .._helpers import SideSelector, TickerSelector, add_order, describe_price_test


def prepare_orders_before_test(
    processor: order_processing.OrderBookProcessor,
    ticker_selector: TickerSelector,
    num_of_additions: int,
) -> None:
    side_selector = SideSelector()
    for idx in range(num_of_additions):
        add_order(
            processor=processor, idx=idx, side=side_selector(), ticker=ticker_selector()
        )


def run_best_price_api_scenario(
    description_suffix: str,
    storage: order_processing.OrderStorage,
    num_of_additions: int,
    num_of_price_api_calls: int,
    num_of_tickers: int,
) -> None:
    describe_price_test(
        name=description_suffix + " - best api scenario",
        price_api_calls=num_of_price_api_calls,
        orders=num_of_additions,
        num_of_tickers=num_of_tickers,
    )
    order_viewer = storage.get_price_view()
    ticker_selector = TickerSelector(num_of_tickers=num_of_tickers)

    print("Preparing orders before test")
    prepare_orders_before_test(
        processor=storage.get_processor(),
        ticker_selector=ticker_selector,
        num_of_additions=num_of_additions,
    )
    print("Orders prepared, starting test")

    with check_perf():
        for _ in range(num_of_price_api_calls):
            order_processing.get_best_bid_and_ask(
                order_book=order_viewer, ticker=ticker_selector()
            )
