from .concrete_order_database import ConcreteOrderDatabase
from .database_order_storage import DatabaseOrderStorage
from .order_storage import OrderStorage


def create_db_order_storage() -> OrderStorage:
    return DatabaseOrderStorage(
        database=ConcreteOrderDatabase(database_name=":memory:")
    )
