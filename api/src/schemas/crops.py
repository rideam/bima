from tortoise.contrib.pydantic import pydantic_model_creator

from src.database.models import Crops

CropInSchema = pydantic_model_creator(
    Crops,
    name="CropIn",
    exclude_readonly=True
)

CropOutSchema = pydantic_model_creator(
    Crops,
    name="CropOut",
    exclude=[
        "created_at",
        "modified_at",
        "weather",
        "policies.created_at",
        "policies.modified_at",
        "policies"
    ]
)

CropDatabaseSchema = pydantic_model_creator(
    Crops,
    name="Crop",
    exclude=[
        "created_at",
        "modified_at"
    ]
)
