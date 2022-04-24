from interview_2022_03_28 import order_processing

from .scenarios.best_price_api_scenario import run_best_price_api_scenario

NUM_OF_TICKERS = 1

if __name__ == "__main__":
    run_best_price_api_scenario(
        description_suffix="Database",
        storage=order_processing.create_db_order_storage(),
        num_of_additions=100_000,
        num_of_price_api_calls=100,
        num_of_tickers=NUM_OF_TICKERS,
    )

    run_best_price_api_scenario(
        description_suffix="RedBlackTree",
        storage=order_processing.create_tree_order_storage(),
        num_of_additions=1_000_000,
        num_of_price_api_calls=1_000_000,
        num_of_tickers=NUM_OF_TICKERS,
    )
