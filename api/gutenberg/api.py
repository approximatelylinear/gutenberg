from typing import Union

from fastapi import FastAPI, Query

from gutenberg.client import make_client
from gutenberg.es_index import EsIndex
from gutenberg.search import Searcher


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



@app.get("/search")
def search(
        index: str,
        query: str,
        page_number: int = Query(1, ge=1),
        highlight: bool = False
    ):
    es_client = make_client()
    searcher = Searcher(es_index=EsIndex(es_client, index))
    hits = searcher.search(
        query, highlight=highlight, page_number=page_number
    )
    total_results = len(hits)
    total_pages = 1  # Assuming 1 page for now
    current_page_results = hits

    response = {
        "current_page": current_page_results,
        "highlighted": highlight,
        "total_results": total_results,
        "total_pages": total_pages
    }

    return response
