from interview_2022_03_28 import order_processing

from .scenarios.modification_procesures_scenario import (
    run_modification_procesures_scenario,
)

NUM_OF_TICKERS = 1

if __name__ == "__main__":
    run_modification_procesures_scenario(
        test_name="Database - additions & updates & cancels, single ticker",
        storage=order_processing.create_db_order_storage(),
        num_of_additions=100_000,
        num_of_updates=100_000,
        num_of_cancels=100_000,
        num_of_tickers=NUM_OF_TICKERS,
    )

    run_modification_procesures_scenario(
        test_name="RedBlackTree - additions & updates & cancels, single ticker",
        storage=order_processing.create_tree_order_storage(),
        num_of_additions=100_000,
        num_of_updates=100_000,
        num_of_cancels=100_000,
        num_of_tickers=NUM_OF_TICKERS,
    )
