from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Farms

FarmInSchema = pydantic_model_creator(
    Farms,
    name="FarmIn",
    exclude=["user_id"],
    exclude_readonly=True
)

FarmOutSchema = pydantic_model_creator(
    Farms,
    name="FarmOut",
    exclude=[
        "created_at",
        "modified_at",
        "region.created_at",
        "region.modified_at",
        "weather"
    ]
)

FarmDatabaseSchema = pydantic_model_creator(
    Farms,
    name="Farm",
    exclude=["created_at", "modified_at"]
)
