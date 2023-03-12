from datetime import datetime
from typing import Optional

import typer

from query import QueryOption, Query

app = typer.Typer()


@app.command()
def fuzzy(option: QueryOption = typer.Argument(...), key: str = typer.Argument(...),
          value: str = typer.Argument(...), fuzziness: str = typer.Argument(default='AUTO')):
    with Query.load() as query:
        query.add_fuzzy(option, key, value, fuzziness)


@app.command()
def cost_range(option: QueryOption = typer.Argument(...), gte: float = typer.Argument(default=None),
               lte: float = typer.Argument(default=None), ):
    with Query.load() as query:
        if gte is None and lte is None:
            print("WARNING: both gte and lte is not set, skipping range addition")
            pass
        query.add_range(option, "cost", gte, lte)


@app.command()
def release_date_range(option: QueryOption = typer.Argument(...), gte: datetime = typer.Argument(default=None),
                       lte: datetime = typer.Argument(default=None), ):
    with Query.load() as query:
        if gte is None and lte is None:
            print("WARNING: both gte and lte is not set, skipping range addition")
            pass
        query.add_range(option, "release_date", gte.date(), lte.date())


@app.command()
def term(option: QueryOption = typer.Argument(...), key: str = typer.Argument(...),
         value: str = typer.Argument(...)):
    with Query.load() as query:
        query: Query
        query.add_term(option, key, value)


@app.command()
def match(option: QueryOption = typer.Argument(...), key: str = typer.Argument(...),
          value: str = typer.Argument(...)):
    with Query.load() as query:
        query: Query
        query.add_match(option, key, value)
