import uuid
from dataclasses import asdict
from datetime import datetime
from contextlib import contextmanager
from typing import Generator

import typer
from elasticsearch import Elasticsearch

import add_query
from painting import Painting
from query import Query
from settings import INDEX

app = typer.Typer()

app.add_typer(add_query.app, name="add-query")


@contextmanager
def connect_es() -> Generator[Elasticsearch, None, None]:
    es = Elasticsearch("http://localhost:9200")
    try:
        yield es
    finally:
        es.transport.close()


@app.command()
def create_document(
        name: str = typer.Option(...),
        release_date: datetime = typer.Option(...),
        genres: list[str] = typer.Option(...),
        cost: int = typer.Option(...),
) -> None:
    with connect_es() as es:
        es: Elasticsearch
        document = Painting(name=name, release_date=release_date.date(), genres=genres, cost=cost).to_dict()
        response = es.index(index=INDEX, id=str(uuid.uuid4()), document=document)
        print(response['result'])


@app.command()
def delete_document(id: str = typer.Argument(...)) -> None:
    with connect_es() as es:
        es: Elasticsearch
        response = es.delete(index=INDEX, id=id)
        print(response['result'])


@app.command()
def index_mapping(force_delete: bool = typer.Option(default=False)):
    with connect_es() as es:
        es: Elasticsearch
        if force_delete:
            es.options(ignore_status=[400, 404]).indices.delete(index=INDEX)
        es.indices.create(index=INDEX, mappings=Painting.mapping)


@app.command()
def search_name(name: str = typer.Argument(...)):
    with connect_es() as es:
        res = es.search(index=INDEX, query={"fuzzy": {"name": {"value": name}}})
        for hit in res['hits']['hits']:
            print(Painting(**hit['_source'], _id=hit['_id'], _score=hit['_score']))


@app.command()
def search(display_texts: bool = typer.Option(default=False)):
    with Query.load() as query:
        query: Query
        search_query = query.to_dict()
        print(search_query)
        with connect_es() as es:
            res = es.search(index=INDEX, query=search_query)
            for hit in res['hits']['hits']:
                painting = Painting(**hit['_source'], _id=hit['_id'], _score=hit['_score'])
                print(painting)


@app.command()
def reset_query():
    Query.reset_query()


if __name__ == "__main__":
    app()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
