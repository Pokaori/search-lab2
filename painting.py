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
    description: str
    specification: str
    history: str

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
            "specification": {
                "type": "text",
                "analyzer": "custom_analyzer"
            },
            "history": {
                "type": "text",
                "analyzer": "english"
            },
            "description": {
                "type": "text",
                "analyzer": "standard"
            }
        }
    }

    def to_dict(self) -> {str, Any}:
        return {k: v for k, v in asdict(self).items() if v}
