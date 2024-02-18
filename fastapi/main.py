from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import phonebook
from core.config import settings
from db import current_storage
from db.redis import AsyncRedisStorageEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    current_storage.current_storage = AsyncRedisStorageEngine()
    yield
    await current_storage.current_storage.close()


tags_metadata = [
    {
        "name": "phonebook",
        "description": "Operations with phonebook records",
    },
]
openapi_url="/openapi.json" if settings.show_openapi_docs else None
app = FastAPI(
    title="Phonebook",
    summary="An API application for storing and editing phonebook records",
    version="1.0.0",
    openapi_tags=tags_metadata,
    openapi_url=openapi_url,
    lifespan=lifespan,
)
app.include_router(phonebook.router, prefix="", tags=["phonebook"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
