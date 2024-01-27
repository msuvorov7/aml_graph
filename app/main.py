import logging
import os
import sys

import arango
import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

app = FastAPI()
app.mount(
    "/static",
    StaticFiles(directory=Path(__file__).parent.parent.absolute() / "static"),
    name="static",
)
templates = Jinja2Templates(directory="../templates")


class TraversalFormData(BaseModel):
    """ Validate request data """
    idField: str
    maxDepth: int
    bfsDirection: str
    searchID: str


@app.get("/")
async def main(request: Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.get('/about')
async def about(request: Request):
    logging.info('about')
    return templates.TemplateResponse("about.html", context={"request": request})


if __name__ == '__main__':
    client = arango.ArangoClient()
    db = client.db(name='_system', username='root', password='root')
    logging.info('Connected to DB')
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", "80")), log_level="info")
