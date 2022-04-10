import sqlite3
from typing import List

from .order import Order
from .order_database import OrderDatabase


class DatabaseTableAlreadyExistsError(Exception):
    pass


class DatabaseTableCreationError(Exception):
    pass


class ConcreteOrderDatabase(OrderDatabase):
    def __init__(self, database_name: str) -> None:
        self.__connection = sqlite3.connect(database=database_name)
        self.__cursor = self.__connection.cursor()

    def __del__(self) -> None:
        self.__connection.close()

    def create_table(self, name: str, columns) -> None:
        if self.__does_table_exist(name=name):
            raise DatabaseTableAlreadyExistsError(f"Table {name} already exists!")

        joined_columns = ", ".join([f"{key} {val}" for key, val in columns.items()])
        query = f"create table {name} ({joined_columns})"

        try:
            self.__cursor.execute(query)
        except Exception as err:
            raise DatabaseTableCreationError(
                f"Cannot create table {name} with columns: {columns}"
            ) from err

    def insert(self, order: Order) -> None:
        self.__cursor.execute(
            "insert into orders values (?, ?, ?, ?, ?, ?)",
            (
                order.order_id,
                order.timestamp,
                order.ticker,
                order.price,
                order.size,
                order.order_type.name,
            ),
        )
        self.__connection.commit()

    def remove(self, order_id: str) -> None:
        self.__cursor.execute("delete from orders where order_id=?", (order_id,))

    def update(self, order_id: str, size: int) -> None:
        self.__cursor.execute(
            "update orders set size = :size where order_id=:order_id",
            {"order_id": order_id, "size": size},
        )

    def has_order(self, order_id: str) -> bool:
        self.__cursor.execute(
            "select order_id from orders where order_id=?", (order_id,)
        )

        result = self.__cursor.fetchone()
        return result is not None

    def get_best_ask(self, ticker: str) -> float:
        self.__cursor.execute(
            """select price from orders where type='ASK' and ticker=?
            order by price limit 1""",
            (ticker,),
        )
        result = self.__cursor.fetchone()
        return 0.0 if result is None else result[0]

    def get_best_bid(self, ticker: str) -> float:
        self.__cursor.execute(
            """select price from orders where type='BID' and ticker=?
            order by price desc limit 1""",
            (ticker,),
        )
        result = self.__cursor.fetchone()
        return 0.0 if result is None else result[0]

    def fetch_orders(self) -> list:
        self.__cursor.execute("select * from orders")
        return self.__cursor.fetchall()

    def fetch_column(self, column: str) -> list:
        self.__cursor.execute(f"select {column} from orders")
        return self.__cursor.fetchall()

    def fetch_columns(self, columns: List[str]) -> list:
        selected_columns = ", ".join(columns)
        self.__cursor.execute(f"select {selected_columns} from orders")
        return self.__cursor.fetchall()

    def __does_table_exist(self, name: str) -> bool:
        self.__cursor.execute(
            "select count(name) from sqlite_master where type='table' and name=?",
            (name,),
        )
        num_of_orders_tables = self.__cursor.fetchone()[0]
        return num_of_orders_tables > 0
