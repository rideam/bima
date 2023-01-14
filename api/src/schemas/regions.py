from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Regions

RegionInSchema = pydantic_model_creator(
    Regions,
    name="RegionIn",
    exclude_readonly=True
)

RegionOutSchema = pydantic_model_creator(
    Regions,
    name="RegionOut",
    exclude=[
        "created_at",
        "modified_at",
        "farms.weather",
        "farms.created_at",
        "farms.modified_at",
    ]
)

RegionDatabaseSchema = pydantic_model_creator(
    Regions,
    name="Region",
    exclude=["created_at", "modified_at"]
)
