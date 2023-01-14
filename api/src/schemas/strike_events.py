from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import StrikeEvents

StrikeEventInSchema = pydantic_model_creator(
    StrikeEvents,
    name="StrikeEventIn",
    exclude_readonly=True
)

StrikeEventOutSchema = pydantic_model_creator(
    StrikeEvents,
    name="StrikeEventOut",
    exclude=[
        "created_at",
        "modified_at",
    ]
)

StrikeEventDatabaseSchema = pydantic_model_creator(
    StrikeEvents,
    name="StrikeEvent",
    exclude=[
        "created_at",
        "modified_at"
    ]
)
