import logging
from typing import Optional

from fastapi import FastAPI

from app.config import get_settings

settings = get_settings()
app = FastAPI()


@app.get("/")
def read_root():
    logging.info(f"Called read_root function in {settings.app_name}")
    return {"Hello": settings.app_name}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
