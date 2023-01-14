from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Weather

WeatherInSchema = pydantic_model_creator(
    Weather,
    name="WeatherIn",
    exclude=[],
    exclude_readonly=True
)

WeatherOutSchema = pydantic_model_creator(
    Weather,
    name="WeatherOut",
    exclude=[
        "created_at",
        "modified_at",
        "farm.created_at",
        "farm.modified_at",
        "crop.created_at",
        "crop.policies",
        "crop.modified_at"
    ]
)

WeatherDatabaseSchema = pydantic_model_creator(
    Weather,
    name="Weather",
    exclude=["created_at", "modified_at"]
)
