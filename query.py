from settings import QUERY_PATH
from typing import Any, Optional, Generator, Union, TypeAlias
from dataclasses import dataclass, field, asdict
from enum import Enum
import json
from contextlib import contextmanager
import os
from datetime import date

QueryOperator: TypeAlias = dict[str, Any]


class QueryOption(str, Enum):
    must = "must"
    must_not = "must_not"
    should = "should"
    filter = "filter"


@dataclass()
class Query:
    _must_not: list[QueryOperator] = field(default_factory=list)
    _must: list[QueryOperator] = field(default_factory=list)
    _should: list[QueryOperator] = field(default_factory=list)
    _filter: list[QueryOperator] = field(default_factory=list)

    def _get_option(self, option: QueryOption) -> Optional[list]:
        options = {QueryOption.must: self._must, QueryOption.must_not: self._must_not, QueryOption.should: self._should,
                   QueryOption.filter: self._filter}
        return options.get(option)

    def to_dict(self) -> QueryOperator:
        es_query: dict[str, list[QueryOperator]] = {option.value: [op for op in self._get_option(option)] for option in
                                                    QueryOption if self._get_option(option)}
        return {"bool": es_query}

    def add_fuzzy(self, option: QueryOption, key: str, value: str, fuzziness: str = "AUTO"):
        query_value = self._get_option(option)
        query_value.append({"fuzzy": {key: {"value": value, "fuzziness": fuzziness}}})

    def add_range(self, option: QueryOption, key: str, gte: Optional[Union[float, date]],
                  lte: Optional[Union[float, date]]):
        query_value = self._get_option(option)
        query_value.append({"range": {key: {"gte": gte, "lte": lte}}})

    def add_term(self, option: QueryOption, key: str, value: str):
        query_value = self._get_option(option)
        query_value.append({"term": {key: value}})

    def add_match(self, option: QueryOption, key: str, value: str):
        query_value = self._get_option(option)
        query_value.append({"match": {key: value}})

    def save(self) -> None:
        with open(QUERY_PATH, "w") as f:
            json.dump(asdict(self), f, default=str, indent=4)

    @classmethod
    @contextmanager
    def load(cls) -> Generator['Query', None, None]:
        try:
            with open(QUERY_PATH, "r") as f:
                data = json.load(f)
                query = cls(**data)
        except FileNotFoundError:
            query = cls()
        try:
            yield query
        finally:
            query.save()

    @classmethod
    def reset_query(cls) -> None:
        os.unlink(QUERY_PATH)
