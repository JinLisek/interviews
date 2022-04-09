import pytest

from ..concrete_order_database import ConcreteOrderDatabase
from ..order_book import DatabaseOrderBook


@pytest.fixture(name="database")
def fixture_temporary_database():
    return ConcreteOrderDatabase(database_name=":memory:")


@pytest.fixture(name="order_book")
def fixture_order_book(database):
    return DatabaseOrderBook(database=database)
