import pytest

from ..concrete_order_database import ConcreteOrderDatabase
from ..database_order_book import DatabaseOrderBook
from ..tree_order_book import TreeOrderBook


@pytest.fixture(name="database")
def fixture_temporary_database():
    return ConcreteOrderDatabase(database_name=":memory:")


@pytest.fixture(name="order_book")
def fixture_order_book(database):
    return DatabaseOrderBook(database=database)


@pytest.fixture(name="tree_order_book")
def fixture_tree_order_book():
    return TreeOrderBook()
