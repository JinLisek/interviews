from .concrete_order_database import ConcreteOrderDatabase
from .order_database import OrderDatabase
from .order_storage import OrderStorage

from .concrete_order_storage import ConcreteOrderStorage


def create_order_database(name: str) -> OrderDatabase:
    return ConcreteOrderDatabase(database_name=name)


def create_order_storage(database: OrderDatabase) -> OrderStorage:
    return ConcreteOrderStorage(database=database)
