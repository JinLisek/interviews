from ..order_storage import OrderStorage
from .tree_order_storage import TreeOrderStorage


def create_tree_order_storage() -> OrderStorage:
    return TreeOrderStorage()
