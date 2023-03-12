import uuid
from dataclasses import dataclass, field, asdict
from datetime import date
from typing import Optional, Any, ClassVar


@dataclass
class Painting:
    name: str
    release_date: date
    genres: list[str]
    cost: int

    _id: Optional[str] = None
    _score: Optional[float] = None
    mapping: ClassVar[dict] = {
        "properties": {
            "name": {
                "type": "keyword"
            },
            "genres": {
                "type": "keyword"
            },
            "cost": {
                "type": "integer"
            },
            "release_date": {
                "type": "date"
            },
        }
    }

    def to_dict(self) -> {str, Any}:
        return {k: v for k, v in asdict(self).items() if v}
