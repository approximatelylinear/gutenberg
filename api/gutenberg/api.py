from typing import Union
import logging
import sys

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response

from gutenberg.client import make_client
from gutenberg.es_index import EsIndex
from gutenberg.search import Searcher
from gutenberg.settings import FRONTEND_URL


loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
for logger in loggers:
    print(f'setting {logger.name} to DEBUG')
    logger.setLevel(logging.DEBUG)

app = FastAPI()

@app.middleware("http")
async def log_requests(request, call_next):
    # Log details of the incoming request
    print("Request received:")
    print("Method:", request.method)
    print("URL:", request.url)
    print("Headers:", request.headers)
    print("Query parameters:", request.query_params)
    print("Path parameters:", request.path_params)

    # Continue handling the request
    response = await call_next(request)

    # Log details of the response
    print("Response sent:")
    print("Status code:", response.status_code)
    print("Headers:", response.headers)

    return response


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    print('read_root')
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
    try:
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
    except Exception as e:
        response = {
            "error": str(e)
        }
    response = JSONResponse(response)
    return response
