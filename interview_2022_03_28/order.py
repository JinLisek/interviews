from dataclasses import dataclass
from enum import Enum, unique


@unique
class OrderType(Enum):
    BID = "BID"
    ASK = "ASK"


@dataclass
class Order:
    order_id: str
    timestamp: str
    ticker: str
    price: float
    size: int
    order_type: OrderType
