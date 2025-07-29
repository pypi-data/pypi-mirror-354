import os
from enum import Enum
from typing import Any, Callable
from ._drivers import _setup_db, _insert_row, _fetch_all_rows, Row


class DatabaseParameterType(Enum):
    STRING = "TEXT"
    INT = "INTEGER"
    FLOAT = "REAL"
    BOOLEAN = "INTEGER"


class DatabaseParameter:
    def __init__(self, key: str, valueType: DatabaseParameterType):
        if not isinstance(valueType, DatabaseParameterType):
            raise ValueError("valueType must be a DatabaseParameterType")
        self.key = key
        self.valueType = valueType


class Database:
    def __init__(self, name: str, parameters: list[DatabaseParameter]):
        self.name = name
        self.parameters = parameters

        base_path = os.path.join(os.path.dirname(__file__), "_databases")
        if not os.path.isdir(base_path):
            raise FileNotFoundError(f"Expected database folder is missing: {base_path}")

        self.db_path = os.path.join(base_path, f"_{name}.db")

    def setup(self):
        _setup_db(self)

    def add_row(self, **kwargs: Any):
        _insert_row(self, kwargs)

    def query(self, predicate: Callable[[Row], bool]) -> list[Row]:
        return [row for row in _fetch_all_rows(self) if predicate(row)]
