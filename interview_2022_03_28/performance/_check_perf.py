from contextlib import contextmanager
from time import perf_counter


@contextmanager
def check_perf():
    start_time = perf_counter()
    yield
    stop_time = perf_counter()
    print(f"Took {stop_time- start_time} seconds")
