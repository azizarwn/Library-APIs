from fastapi import FastAPI
from scalar_fastapi import get_scalar_api_reference

from app.core.settings import settings
from app.router.books import books_router
from app.router.borrowing_records import borrow_router
from app.router.members import members_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    docs_url=None,
    redoc_url=None,
)

app.include_router(router=books_router)
app.include_router(router=borrow_router)
app.include_router(router=members_router)


@app.get("/")
def root():
    return {
        "message": "Library Management API",
        "docs": "/scalar",
        "endpoints": {"books": "/books/", "members": "/members/", "borrowing_records": "/borrowing_records/"},
    }


@app.get(path="/scalar")
def get_scalar():
    return get_scalar_api_reference(openapi_url=app.openapi_url, title=app.title)
