from ..order_storage import OrderStorage
from .concrete_order_database import ConcreteOrderDatabase
from .database_order_storage import DatabaseOrderStorage


def create_db_order_storage() -> OrderStorage:
    return DatabaseOrderStorage(
        database=ConcreteOrderDatabase(database_name=":memory:")
    )
