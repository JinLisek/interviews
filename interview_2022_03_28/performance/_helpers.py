import calendar
import itertools
import random
import time
from typing import List

from interview_2022_03_28 import order_processing


def add_order(
    processor: order_processing.OrderBookProcessor, idx: int, side: str, ticker: str
) -> None:
    order = create_add_order(idx=idx, side=side, ticker=ticker)
    order_processing.process_order(order_book=processor, order=order)


def update_order(processor: order_processing.OrderBookProcessor, idx: int) -> None:
    order = create_update_order(idx=idx)
    order_processing.process_order(order_book=processor, order=order)


def cancel_order(processor: order_processing.OrderBookProcessor, idx: int) -> None:
    order = create_cancel_order(idx=idx)
    order_processing.process_order(order_book=processor, order=order)


def create_add_order(idx: int, side: str, ticker: str) -> str:
    order_id = idx_to_order_id(idx=idx)
    timestamp = current_timestamp()
    return (
        f"{timestamp}|{order_id}|a|{ticker}|{side}|{random_price()}|{random_add_size()}"
    )


def create_update_order(idx: int) -> str:
    order_id = idx_to_order_id(idx=idx)
    timestamp = current_timestamp()
    return f"{timestamp}|{order_id}|u|{random_update_size()}"


def create_cancel_order(idx: int) -> str:
    order_id = idx_to_order_id(idx=idx)
    timestamp = current_timestamp()
    return f"{timestamp}|{order_id}|c"


class SideSelector:
    def __init__(self) -> None:
        self.__last_side_buy = False

    def __call__(self) -> str:
        if self.__last_side_buy:
            self.__last_side_buy = False
            return "S"
        self.__last_side_buy = True
        return "B"


class TickerSelector:
    def __init__(self, num_of_tickers) -> None:
        self.__tickers = generate_tickers(num_of_tickers=num_of_tickers)
        self.__iterator = itertools.cycle(self.__tickers)

    def __call__(self) -> str:
        return next(self.__iterator)


class IdGenerator:
    def __init__(self) -> None:
        self.__current_id = 0

    def __call__(self) -> str:
        return hex(self.__current_id)[2:]


def random_price() -> float:
    return random.uniform(1.0, 99.9)


def random_add_size() -> int:
    return random.randint(1, 999)


def random_update_size() -> int:
    return random.randint(1000, 1999)


def current_timestamp() -> int:
    return calendar.timegm(time.gmtime())


def idx_to_order_id(idx: int) -> str:
    return hex(idx)[2:]


def generate_tickers(num_of_tickers: int) -> List[str]:
    return [hex(idx)[2:] for idx in range(num_of_tickers)]


def describe_test(name: str, additions: int, updates: int, cancels: int) -> None:
    print(f"Running test: {name}")
    print(f"Number of additions: {format_int(additions)}")
    print(f"Number of updates: {format_int(updates)}")
    print(f"Number of cancels: {format_int(cancels)}")


def describe_price_test(
    name: str, price_api_calls: int, orders: int, num_of_tickers: int
) -> None:
    print(f"Running test: {name}")
    print(f"Number of prepared orders: {format_int(orders)}")
    print(f"Number of best bid/ask calls: {format_int(price_api_calls)}")
    print(f"Number of tickers: {format_int(num_of_tickers)}")


def format_int(val: int) -> str:
    return f"{val:,}".replace(",", " ")
