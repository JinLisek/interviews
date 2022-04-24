import pytest

from ..tree_order_book import TreeOrderBook


@pytest.fixture(name="tree_order_book")
def fixture_tree_order_book() -> TreeOrderBook:
    return TreeOrderBook()
