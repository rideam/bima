from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from tortoise import Tortoise
from src.database.register import register_tortoise
from src.database.config import TORTOISE_ORM

Tortoise.init_models(["src.database.models"], "models")

from src.routes import \
    users, \
    weather, \
    regions, \
    crops, \
    farmers, \
    farms, \
    strike_events, \
    policies

description = """
Weather crop index insurance API

"""

tags_metadata = [
    {
        "name": "Auth",
        "description": "User Authentication"
    },
    {
        "name": "Region",
        "description": "Region data"
    },
    {
        "name": "Crop",
        "description": "Crop data"
    },
    {
        "name": "Farm",
        "description": "Farm data"
    },
    {
        "name": "Weather",
        "description": "Weather data"
    },
    {
        "name": "StrikeEvent",
        "description": "StrikeEvent data"
    },
    {
        "name": "Policy",
        "description": "Policy data"
    },
    {
        "name": "User",
        "description": "User actions"
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

app.include_router(users.router)
app.include_router(weather.router)
app.include_router(regions.router)
app.include_router(crops.router)
app.include_router(farmers.router)
app.include_router(farms.router)
app.include_router(strike_events.router)
app.include_router(policies.router)

register_tortoise(app, config=TORTOISE_ORM, generate_schemas=False)


@app.get("/", include_in_schema=False)
def home():
    return RedirectResponse(url="/docs/")


@app.get("/ping", include_in_schema=False)
def ping():
    return "API is running successfully"
