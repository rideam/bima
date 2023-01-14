from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import AccessLevels

AccessLevelInSchema = pydantic_model_creator(
    AccessLevels,
    name="AccessLevelIn",
    exclude_readonly=True
)

AccessLevelOutSchema = pydantic_model_creator(
    AccessLevels,
    name="AccessLevelOut",
    exclude=[
        "created_at",
        "modified_at",
    ]
)

AccessLevelDatabaseSchema = pydantic_model_creator(
    AccessLevels,
    name="AccessLevel",
    exclude=[
        "created_at",
        "modified_at"
    ]
)
