from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse
from .routes import router

from . import models
from .db import engine

models.Base.metadata.create_all(bind=engine)

description = """
Weather crop index insurance API

"""

tags_metadata = [
    {
        "name": "Function",
        "description": "Get index data and peform calculations to get statistics"
    },
    {
        "name": "Utilities",
        "description": "Utility routes for other needed information"
    }
]

app = FastAPI(
    title="BIMA",
    description=description,
    version="1.0.0",
    openapi_tags=tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url="/docs/")


@app.get("/ping", include_in_schema=False)
def ping():
    return "API is running successfully"
