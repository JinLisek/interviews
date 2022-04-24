from interview_2022_03_28 import order_processing

from .scenarios.modification_procesures_scenario import (
    run_modification_procesures_scenario,
)

NUM_OF_TICKERS = 2_000

if __name__ == "__main__":
    run_modification_procesures_scenario(
        test_name="Database - only additions, multiple tickers",
        storage=order_processing.create_db_order_storage(),
        num_of_additions=200_000,
        num_of_updates=0,
        num_of_cancels=0,
        num_of_tickers=NUM_OF_TICKERS,
    )

    run_modification_procesures_scenario(
        test_name="RedBlackTree - only additions, multiple tickers",
        storage=order_processing.create_tree_order_storage(),
        num_of_additions=200_000,
        num_of_updates=0,
        num_of_cancels=0,
        num_of_tickers=NUM_OF_TICKERS,
    )
